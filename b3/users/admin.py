from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        ("User", {"fields": ("email", "password")}),
        (
            _("Personal"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    exclude = ("username",)
    list_display = ("email", "first_name", "last_name", "created_at")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)

        # Read only if the user is not a superuser, and they are editing another staff user (not themselves)
        if (
            not request.user.is_superuser
            and obj is not None
            and obj.is_staff
            and obj != request.user
        ):
            return (
                readonly_fields
                + tuple(field.name for field in obj._meta.fields)
                + ("groups", "user_permissions")
            )

        # Make specific fields read-only for non-superusers
        if not request.user.is_superuser:
            readonly_fields += (
                "is_superuser",
                "is_staff",
                "groups",
                "user_permissions",
            )

        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        # Prevent non-superusers from deleting staff users (including themselves)
        if obj is not None and obj.is_staff:
            return False

        return super().has_delete_permission(request, obj)
