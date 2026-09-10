from django.contrib import admin

from .models import Certificate, TeacherProfile


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 0


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "region", "comuna", "is_bilingual", "is_active")
    list_filter = ("is_active", "is_bilingual", "region", "available_short", "available_long")
    search_fields = ("full_name", "user__email", "phone")
    filter_horizontal = ("subjects", "preferred_comunas")
    inlines = [CertificateInline]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("name", "doc_type", "profile", "uploaded_at")
    list_filter = ("doc_type",)
    search_fields = ("name", "profile__full_name")
