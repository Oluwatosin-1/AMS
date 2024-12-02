from django.contrib import admin
from .models import Payment, Payout

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'amount', 'status', 'payment_date')
    list_filter = ('status',)
    search_fields = ('affiliate__user__username',)
    ordering = ('payment_date',)
 
@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'amount', 'processed_at', 'status', 'reference_id')
    list_filter = ('status', 'processed_at')
    search_fields = ('affiliate__user__username', 'reference_id')
