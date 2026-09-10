from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView

from .forms import ApplicantRegistrationForm, SchoolRegistrationForm


class _RegisterView(CreateView):
    template_name = "registration/register.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        # Preserve ?next= (used by the school invitation flow).
        nxt = self.request.GET.get("next")
        return nxt or reverse("post_login_redirect")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault("heading", self.heading)
        ctx.setdefault("subtitle", self.subtitle)
        return ctx


class ApplicantRegisterView(_RegisterView):
    form_class = ApplicantRegistrationForm
    heading = "Crear cuenta de profe"
    subtitle = "Postula para hacer reemplazos. Completa tu perfil y súbelo a la base."


class SchoolRegisterView(_RegisterView):
    form_class = SchoolRegistrationForm
    heading = "Crear cuenta de colegio"
    subtitle = "Encuentra profesores evaluados y disponibles para reemplazos."


@login_required
def post_login_redirect(request):
    """Route each user to the right home after login based on their role."""
    user = request.user
    if user.is_superuser or user.role == "staff":
        return redirect("evaluations:queue")
    if user.role == "applicant":
        return redirect("teachers:dashboard")
    if user.role == "school":
        # Send to directory if they already belong to a school, else onboarding.
        if user.school_memberships.exists():
            return redirect("schools:directory")
        return redirect("schools:onboarding")
    return redirect("home")


def register_choice(request):
    """Landing choice between the two self-service registration types."""
    return render(request, "registration/register_choice.html")
