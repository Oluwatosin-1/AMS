from django.contrib import admin
from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'client_email', 'commission_earned', 'referred_at')
    list_filter = ('referred_at',)
    search_fields = ('affiliate__user__username', 'client_email')
    ordering = ('referred_at',)
