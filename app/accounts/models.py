from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """Custom user: email is the login identifier and `role` drives access."""

    class Roles(models.TextChoices):
        APPLICANT = "applicant", _("Postulante (profe)")
        SCHOOL = "school", _("Colegio")
        STAFF = "staff", _("Evaluador/a (sicóloga)")
        ADMIN = "admin", _("Administrador")

    # Drop username; use email instead.
    username = None
    email = models.EmailField(_("correo electrónico"), unique=True)
    role = models.CharField(
        _("rol"), max_length=20, choices=Roles.choices, default=Roles.APPLICANT
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # --- Convenience role checks ---
    @property
    def is_applicant(self):
        return self.role == self.Roles.APPLICANT

    @property
    def is_school(self):
        return self.role == self.Roles.SCHOOL

    @property
    def is_staff_evaluator(self):
        return self.role == self.Roles.STAFF or self.is_superuser
