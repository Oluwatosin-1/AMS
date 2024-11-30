from django.contrib import admin
from .models import CustomUser, Affiliate

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('user', 'commission_rate', 'training_completed', 'referrals', 'payout_threshold')
    list_filter = ('training_completed',)
    search_fields = ('user__username', 'user__email')
    ordering = ('user',)
