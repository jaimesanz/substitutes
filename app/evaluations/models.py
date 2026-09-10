from django.conf import settings
from django.db import models
from django.utils import timezone


class Evaluation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        APPROVED = "approved", "Aprobado"
        REJECTED = "rejected", "Rechazado"

    profile = models.OneToOneField(
        "teachers.TeacherProfile", on_delete=models.CASCADE, related_name="evaluation"
    )
    status = models.CharField(
        "estado", max_length=20, choices=Status.choices, default=Status.PENDING
    )
    rating = models.PositiveSmallIntegerField(
        "evaluación (1-5)", null=True, blank=True,
        help_text="Puntaje otorgado por la evaluadora.",
    )
    notes = models.TextField("notas internas", blank=True)
    evaluated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="evaluations_made", verbose_name="evaluado por",
    )
    evaluated_at = models.DateTimeField("fecha de evaluación", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "evaluación"
        verbose_name_plural = "evaluaciones"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.profile} — {self.get_status_display()}"

    @property
    def is_approved(self):
        return self.status == self.Status.APPROVED

    def mark(self, status, rating, notes, evaluator):
        self.status = status
        self.rating = rating
        self.notes = notes
        self.evaluated_by = evaluator
        self.evaluated_at = timezone.now()
        self.save()
