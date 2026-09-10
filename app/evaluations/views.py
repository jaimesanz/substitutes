from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from core.mixins import StaffRequiredMixin
from teachers.models import TeacherProfile

from .forms import EvaluationForm
from .models import Evaluation


def _ensure_evaluations():
    """Backfill an Evaluation row for any profile missing one."""
    missing = TeacherProfile.objects.filter(evaluation__isnull=True)
    Evaluation.objects.bulk_create([Evaluation(profile=p) for p in missing])


class QueueView(StaffRequiredMixin, View):
    def get(self, request):
        _ensure_evaluations()
        status = request.GET.get("estado", "pending")
        evaluations = Evaluation.objects.select_related(
            "profile", "profile__user", "profile__region"
        )
        if status in dict(Evaluation.Status.choices):
            evaluations = evaluations.filter(status=status)
        counts = {
            "pending": Evaluation.objects.filter(status="pending").count(),
            "approved": Evaluation.objects.filter(status="approved").count(),
            "rejected": Evaluation.objects.filter(status="rejected").count(),
        }
        return render(request, "evaluations/queue.html", {
            "evaluations": evaluations.order_by("profile__full_name"),
            "current_status": status,
            "counts": counts,
        })


class EvaluateView(StaffRequiredMixin, View):
    def _get_objects(self, pk):
        profile = get_object_or_404(
            TeacherProfile.objects.select_related("user", "region", "comuna"), pk=pk
        )
        evaluation, _ = Evaluation.objects.get_or_create(profile=profile)
        return profile, evaluation

    def get(self, request, pk):
        profile, evaluation = self._get_objects(pk)
        form = EvaluationForm(instance=evaluation)
        return render(request, "evaluations/evaluate.html", {
            "profile": profile,
            "evaluation": evaluation,
            "form": form,
            "certificates": profile.certificates.all(),
        })

    def post(self, request, pk):
        profile, evaluation = self._get_objects(pk)
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.evaluated_by = request.user
            from django.utils import timezone
            ev.evaluated_at = timezone.now()
            ev.save()
            messages.success(request, f"Evaluación guardada para {profile.full_name}.")
            return redirect("evaluations:queue")
        return render(request, "evaluations/evaluate.html", {
            "profile": profile,
            "evaluation": evaluation,
            "form": form,
            "certificates": profile.certificates.all(),
        })
