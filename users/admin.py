from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser."""
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'full_name', 'email', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'is_active', 'is_staff'),
        }),
    )
 

class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile."""
    model = UserProfile
    list_display = ('user', 'phone_number', 'city', 'state', 'country', 'preferred_payment_method')
    search_fields = ('user__username', 'user__email', 'city', 'state', 'country')
    ordering = ('user',)


# Register models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
