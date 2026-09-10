import secrets

from django.conf import settings
from django.db import models


def _new_token():
    return secrets.token_urlsafe(32)


class School(models.Model):
    """A colegio: an organization several member users can belong to."""

    name = models.CharField("nombre del colegio", max_length=200)
    rbd = models.CharField("RBD", max_length=20, blank=True,
                           help_text="Rol Base de Datos del establecimiento (opcional).")
    phone = models.CharField("teléfono", max_length=30, blank=True)
    region = models.ForeignKey(
        "catalog.Region", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="schools", verbose_name="región",
    )
    comuna = models.ForeignKey(
        "catalog.Comuna", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="schools", verbose_name="comuna",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "colegio"
        verbose_name_plural = "colegios"
        ordering = ["name"]

    def __str__(self):
        return self.name


class SchoolMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Administrador del colegio"
        MEMBER = "member", "Miembro"

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="school_memberships",
    )
    school_role = models.CharField(
        "rol en el colegio", max_length=20, choices=Role.choices, default=Role.MEMBER
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "miembro de colegio"
        verbose_name_plural = "miembros de colegio"
        unique_together = ("school", "user")

    def __str__(self):
        return f"{self.user} @ {self.school} ({self.get_school_role_display()})"

    @property
    def is_owner(self):
        return self.school_role == self.Role.OWNER


class SchoolInvitation(models.Model):
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField("email invitado")
    token = models.CharField(max_length=64, unique=True, default=_new_token, editable=False)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="invitations_sent",
    )
    accepted = models.BooleanField("aceptada", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "invitación"
        verbose_name_plural = "invitaciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Invitación a {self.email} — {self.school}"
