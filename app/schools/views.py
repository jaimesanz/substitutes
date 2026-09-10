from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from core.mixins import SchoolRequiredMixin
from teachers.models import TeacherProfile

from .filters import TeacherFilter
from .forms import InvitationForm, SchoolForm
from .models import School, SchoolInvitation, SchoolMembership


def _membership(user):
    return user.school_memberships.select_related("school").first()


class SchoolMemberRequiredMixin(SchoolRequiredMixin):
    """School user who already belongs to a school; else send to onboarding."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "school":
            self.membership = _membership(request.user)
            if self.membership is None:
                return redirect("schools:onboarding")
        return super().dispatch(request, *args, **kwargs)


# --- Onboarding & organization management ---

class OnboardingView(SchoolRequiredMixin, View):
    def get(self, request):
        if _membership(request.user):
            return redirect("schools:directory")
        return render(request, "schools/onboarding.html")


class SchoolCreateView(SchoolRequiredMixin, View):
    def get(self, request):
        if _membership(request.user):
            return redirect("schools:directory")
        return render(request, "schools/school_form.html", {"form": SchoolForm()})

    def post(self, request):
        if _membership(request.user):
            return redirect("schools:directory")
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            SchoolMembership.objects.create(
                school=school, user=request.user,
                school_role=SchoolMembership.Role.OWNER,
            )
            messages.success(request, f"Colegio “{school.name}” creado. ¡Ya puedes buscar profes!")
            return redirect("schools:directory")
        return render(request, "schools/school_form.html", {"form": form})


class MembersView(SchoolMemberRequiredMixin, View):
    def get(self, request):
        school = self.membership.school
        return render(request, "schools/members.html", {
            "school": school,
            "membership": self.membership,
            "members": school.memberships.select_related("user"),
            "invitations": school.invitations.filter(accepted=False),
            "form": InvitationForm(),
        })


class InviteCreateView(SchoolMemberRequiredMixin, View):
    def post(self, request):
        if not self.membership.is_owner:
            messages.error(request, "Solo el administrador del colegio puede invitar.")
            return redirect("schools:members")
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.school = self.membership.school
            invitation.invited_by = request.user
            invitation.save()
            link = request.build_absolute_uri(
                reverse("schools:accept_invite", args=[invitation.token])
            )
            messages.success(
                request,
                f"Invitación creada para {invitation.email}. Comparte este enlace: {link}",
            )
        else:
            messages.error(request, "Email inválido.")
        return redirect("schools:members")


class RemoveMemberView(SchoolMemberRequiredMixin, View):
    def post(self, request, pk):
        if not self.membership.is_owner:
            messages.error(request, "Solo el administrador puede quitar miembros.")
            return redirect("schools:members")
        target = get_object_or_404(
            SchoolMembership, pk=pk, school=self.membership.school
        )
        if target.pk == self.membership.pk:
            messages.error(request, "No puedes quitarte a ti mismo.")
        elif target.is_owner:
            messages.error(request, "No puedes quitar a otro administrador.")
        else:
            target.delete()
            messages.success(request, "Miembro removido.")
        return redirect("schools:members")


class AcceptInvitationView(LoginRequiredMixin, View):
    """Accept an invite link. Anonymous users are routed to register first."""

    def get_login_url(self):
        # Send new users to school registration, returning here afterwards.
        return reverse("register_school")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = f"{self.get_login_url()}?next={request.path}"
            return redirect(login_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, token):
        invitation = get_object_or_404(SchoolInvitation, token=token, accepted=False)
        if request.user.role != "school":
            messages.error(request, "Tu cuenta no es de tipo colegio; no puedes aceptar esta invitación.")
            return redirect("home")
        if _membership(request.user):
            messages.info(request, "Ya perteneces a un colegio.")
            return redirect("schools:directory")

        SchoolMembership.objects.create(
            school=invitation.school, user=request.user,
            school_role=SchoolMembership.Role.MEMBER,
        )
        invitation.accepted = True
        invitation.save(update_fields=["accepted"])
        messages.success(request, f"Te uniste a {invitation.school.name}.")
        return redirect("schools:directory")


# --- Directory (browse the vetted database) ---

class DirectoryView(SchoolMemberRequiredMixin, View):
    def get(self, request):
        base_qs = (
            TeacherProfile.objects
            .filter(is_active=True, evaluation__status="approved")
            .select_related("region", "comuna", "evaluation")
            .prefetch_related("subjects")
            .distinct()
            .order_by("full_name")
        )
        f = TeacherFilter(request.GET, queryset=base_qs)
        paginator = Paginator(f.qs, 24)
        page = paginator.get_page(request.GET.get("page"))
        querystring = request.GET.copy()
        querystring.pop("page", None)
        return render(request, "schools/directory.html", {
            "filter": f,
            "page_obj": page,
            "total": f.qs.count(),
            "querystring": querystring.urlencode(),
        })


class ApplicantDetailView(SchoolMemberRequiredMixin, View):
    def get(self, request, pk):
        profile = get_object_or_404(
            TeacherProfile.objects.select_related("region", "comuna", "evaluation")
            .prefetch_related("subjects", "preferred_comunas", "certificates"),
            pk=pk, is_active=True, evaluation__status="approved",
        )
        return render(request, "schools/applicant_detail.html", {"profile": profile})
