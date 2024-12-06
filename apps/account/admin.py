from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Addresses


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "phone_number", "is_active", "is_admin", "joined_at")
    list_filter = ("is_active", "is_admin", "joined_at")
    search_fields = ("email", "full_name", "phone_number")
    ordering = ("-joined_at",)
    readonly_fields = ("joined_at",)
    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Personal Info", {
            "fields": ("full_name", "birthdate", "phone_number", "default_address")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_admin", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login", "joined_at")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_admin"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions")


@admin.register(Addresses)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "province", "city", "phone_number", "zipcode", "created_at")
    list_filter = ("province", "city", "created_at")
    search_fields = ("title", "province", "city", "postal_address", "phone_number", "zipcode")
    ordering = ("-created_at",)
