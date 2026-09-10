from django.contrib import admin

from .models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("profile", "status", "rating", "evaluated_by", "evaluated_at")
    list_filter = ("status",)
    search_fields = ("profile__full_name", "profile__user__email")
    autocomplete_fields = ()
    readonly_fields = ("created_at", "updated_at")
