from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import EmailAuthenticationForm
from . import views

urlpatterns = [
    path(
        "ingresar/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=EmailAuthenticationForm,
        ),
        name="login",
    ),
    path("salir/", auth_views.LogoutView.as_view(), name="logout"),
    path("post-login/", views.post_login_redirect, name="post_login_redirect"),
    path("registro/", views.register_choice, name="register_choice"),
    path("registro/profe/", views.ApplicantRegisterView.as_view(), name="register_applicant"),
    path("registro/colegio/", views.SchoolRegisterView.as_view(), name="register_school"),
    # Password reset (console/email backend; wired for future SMTP).
    path("password/reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password/reset/enviado/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/completo/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
