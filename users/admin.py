from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
        "full_name",
        "user_type",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("user_type", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "full_name")
    readonly_fields = ("date_joined", "last_login")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("full_name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "user_type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user_username",
        "phone_number",
        "city",
        "state",
        "country",
        "preferred_payment_method",
    )
    list_filter = ("preferred_payment_method", "country", "state")
    search_fields = (
        "user__username",
        "phone_number",
        "city",
        "state",
        "country",
        "tax_identification_number",
    )
    readonly_fields = ("user",)
    fieldsets = (
        (None, {"fields": ("user",)}),
        (
            "Contact Info",
            {"fields": ("phone_number", "address", "city", "state", "country")},
        ),
        (
            "Payment Info",
            {
                "fields": (
                    "preferred_payment_method",
                    "bank_account_details",
                    "tax_identification_number",
                )
            },
        ),
        ("Other Info", {"fields": ("website_url",)}),
    )

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = "User"
