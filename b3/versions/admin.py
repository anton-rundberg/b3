from django.contrib import admin

from . import models


@admin.register(models.Version)
class VersionsAdmin(admin.ModelAdmin):
    list_display = ("minimum_version", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
