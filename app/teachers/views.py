from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from core.mixins import ApplicantRequiredMixin
from evaluations.models import Evaluation

from .forms import CertificateForm, TeacherProfileForm
from .models import Certificate, TeacherProfile


def _get_or_create_profile(user):
    profile, _ = TeacherProfile.objects.get_or_create(
        user=user, defaults={"full_name": user.get_full_name() or "", "contact_email": user.email}
    )
    # Ensure an evaluation record exists (starts as pending).
    Evaluation.objects.get_or_create(profile=profile)
    return profile


class DashboardView(ApplicantRequiredMixin, View):
    def get(self, request):
        profile = _get_or_create_profile(request.user)
        return render(request, "teachers/dashboard.html", {
            "profile": profile,
            "evaluation": profile.evaluation,
            "certificates": profile.certificates.all(),
        })


class ProfileEditView(ApplicantRequiredMixin, View):
    def get(self, request):
        profile = _get_or_create_profile(request.user)
        form = TeacherProfileForm(instance=profile)
        return render(request, "teachers/profile_form.html", {"form": form})

    def post(self, request):
        profile = _get_or_create_profile(request.user)
        form = TeacherProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("teachers:dashboard")
        return render(request, "teachers/profile_form.html", {"form": form})


class CertificateCreateView(ApplicantRequiredMixin, View):
    def post(self, request):
        profile = _get_or_create_profile(request.user)
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.profile = profile
            cert.save()
            messages.success(request, "Documento subido.")
        else:
            messages.error(request, "No se pudo subir el documento. Revisa el archivo.")
        return redirect("teachers:dashboard")


class CertificateDeleteView(ApplicantRequiredMixin, View):
    def post(self, request, pk):
        profile = _get_or_create_profile(request.user)
        cert = get_object_or_404(Certificate, pk=pk, profile=profile)
        cert.file.delete(save=False)
        cert.delete()
        messages.success(request, "Documento eliminado.")
        return redirect("teachers:dashboard")
