from django.contrib import admin

from .models import Comuna, Region, Subject


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order", "name")


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    list_filter = ("region",)
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order", "name")
