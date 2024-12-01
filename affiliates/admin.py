from django.contrib import admin
from .models import Affiliate

@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    """Admin configuration for managing affiliates."""
    model = Affiliate

    # Fields to display in the admin list view
    list_display = (
        'user',
        'commission_rate',
        'training_completed',
        'referrals',
        'payout_threshold',
        'referred_by',
        'created_at',
        'updated_at',
    )

    # Fields to filter in the admin list view
    list_filter = (
        'training_completed',
        'commission_rate',
        'payout_threshold',
        'created_at',
    )

    # Fields to search in the admin list view
    search_fields = (
        'user__username',
        'user__email',
        'referred_by__user__username',
    )

    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')

    # Default ordering in the admin
    ordering = ('-created_at',)

    # Customizable admin form layout
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'referred_by'),
        }),
        ('Affiliate Details', {
            'fields': (
                'commission_rate',
                'training_completed',
                'referrals',
                'payout_threshold',
            ),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

  
