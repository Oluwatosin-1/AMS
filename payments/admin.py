from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'amount', 'status', 'payment_date')
    list_filter = ('status',)
    search_fields = ('affiliate__user__username',)
    ordering = ('payment_date',)
