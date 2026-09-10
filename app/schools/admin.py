from django.contrib import admin

from .models import School, SchoolInvitation, SchoolMembership


class MembershipInline(admin.TabularInline):
    model = SchoolMembership
    extra = 0
    autocomplete_fields = ("user",)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "comuna", "created_at")
    list_filter = ("region",)
    search_fields = ("name", "rbd")
    inlines = [MembershipInline]


@admin.register(SchoolMembership)
class SchoolMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "school_role", "created_at")
    list_filter = ("school_role",)
    search_fields = ("user__email", "school__name")


@admin.register(SchoolInvitation)
class SchoolInvitationAdmin(admin.ModelAdmin):
    list_display = ("email", "school", "accepted", "invited_by", "created_at")
    list_filter = ("accepted",)
    search_fields = ("email", "school__name")
