from django.urls import path

from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("perfil/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("certificados/nuevo/", views.CertificateCreateView.as_view(), name="certificate_add"),
    path("certificados/<int:pk>/eliminar/", views.CertificateDeleteView.as_view(), name="certificate_delete"),
]
