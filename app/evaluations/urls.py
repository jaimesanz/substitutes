from django.urls import path

from . import views

app_name = "evaluations"

urlpatterns = [
    path("", views.QueueView.as_view(), name="queue"),
    path("<int:pk>/", views.EvaluateView.as_view(), name="evaluate"),
]
