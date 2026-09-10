from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    """Require login plus one of `allowed_roles` (superuser always allowed)."""

    allowed_roles: tuple = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if request.user.is_superuser or request.user.role in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("No tienes permiso para acceder a esta sección.")


class ApplicantRequiredMixin(RoleRequiredMixin):
    allowed_roles = ("applicant",)


class SchoolRequiredMixin(RoleRequiredMixin):
    allowed_roles = ("school",)


class StaffRequiredMixin(RoleRequiredMixin):
    allowed_roles = ("staff", "admin")
