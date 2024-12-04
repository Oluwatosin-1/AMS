from django.contrib import admin
from .models import PayoutRequest, Payout, Payment


@admin.register(PayoutRequest)
class PayoutRequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for PayoutRequest model.
    """
    list_display = ('affiliate', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('affiliate__user__username', 'affiliate__user__email')
    readonly_fields = ('created_at',)
    fieldsets = (
        ("Request Details", {
            'fields': ('affiliate', 'amount', 'status')
        }),
        ("Timestamps", {
            'fields': ('created_at',)
        }),
    )


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    """
    Admin configuration for Payout model.
    """
    list_display = ('affiliate', 'amount', 'status', 'processed_at', 'reference_id')
    list_filter = ('status', 'processed_at')
    search_fields = ('affiliate__user__username', 'affiliate__user__email', 'reference_id')
    readonly_fields = ('processed_at', 'created_at')
    fieldsets = (
        ("Payout Details", {
            'fields': ('affiliate', 'amount', 'status', 'reference_id')
        }),
        ("Timestamps", {
            'fields': ('processed_at', 'created_at')
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Payment model.
    """
    list_display = ('affiliate', 'amount', 'status', 'payment_date', 'created_at')
    list_filter = ('status', 'payment_date', 'created_at')
    search_fields = ('affiliate__user__username', 'affiliate__user__email')
    readonly_fields = ('payment_date', 'created_at')
    fieldsets = (
        ("Payment Details", {
            'fields': ('affiliate', 'amount', 'status', 'payment_date')
        }),
        ("Timestamps", {
            'fields': ('created_at',)
        }),
    )
