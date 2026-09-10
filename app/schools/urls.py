from django.urls import path

from . import views

app_name = "schools"

urlpatterns = [
    path("inicio/", views.OnboardingView.as_view(), name="onboarding"),
    path("crear/", views.SchoolCreateView.as_view(), name="create"),
    path("miembros/", views.MembersView.as_view(), name="members"),
    path("miembros/invitar/", views.InviteCreateView.as_view(), name="invite"),
    path("miembros/<int:pk>/quitar/", views.RemoveMemberView.as_view(), name="remove_member"),
    path("invitacion/<str:token>/", views.AcceptInvitationView.as_view(), name="accept_invite"),
    path("profes/", views.DirectoryView.as_view(), name="directory"),
    path("profes/<int:pk>/", views.ApplicantDetailView.as_view(), name="applicant_detail"),
]
