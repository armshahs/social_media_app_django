from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FriendRequest
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "name", "password", "avatar")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password", "avatar"),
            },
        ),
    )
    list_display = ("email", "id", "name", "is_active", "is_staff", "is_superuser")
    ordering = ("email",)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        # Hash the password before saving
        obj.password = make_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


admin.site.register(FriendRequest)
