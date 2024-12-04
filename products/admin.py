from django.contrib import admin
from .models import Product, AffiliateProductLink, ProductPurchase
from django.utils.html import format_html
 
from django.urls import path
from django.http import HttpResponse
from django.db.models import Sum, Count
from .models import ProductPurchase

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    """
    list_display = ('name', 'price', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('name', 'keywords')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Product Information", {
            'fields': ('name', 'description', 'price', 'default_commission', 'category', 'status', 'image', 'sales_note')
        }),
        ("SEO and Keywords", {
            'fields': ('keywords',)
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def status_display(self, obj):
        """Display active/inactive status with color coding."""
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.status else 'red',
            'Active' if obj.status else 'Inactive'
        )
    status_display.short_description = 'Status'


@admin.register(AffiliateProductLink)
class AffiliateProductLinkAdmin(admin.ModelAdmin):
    """
    Admin configuration for AffiliateProductLink model.
    """
    list_display = ('affiliate', 'product', 'unique_url', 'clicks')
    list_filter = ('affiliate', 'product')
    search_fields = ('affiliate__user__username', 'product__name')
    readonly_fields = ('unique_url',)

    def affiliate_username(self, obj):
        """Show affiliate username."""
        return obj.affiliate.user.username
    affiliate_username.short_description = 'Affiliate'


@admin.register(ProductPurchase)
class ProductPurchaseAdmin(admin.ModelAdmin):
    """
    Admin configuration for ProductPurchase model.
    """
    list_display = ('product', 'affiliate', 'client_email', 'amount', 'commission_earned', 'is_paid', 'purchased_at')
    list_filter = ('is_paid', 'purchased_at', 'product')
    search_fields = ('client_email', 'product__name', 'affiliate__user__username', 'paystack_reference')
    readonly_fields = ('commission_earned', 'purchased_at')

    def affiliate_username(self, obj):
        """Show affiliate username."""
        return obj.affiliate.user.username if obj.affiliate else "No Affiliate"
    affiliate_username.short_description = 'Affiliate Username'
 
### **Including Sales History for All Affiliate Sales**


class SalesHistoryAdminView(admin.ModelAdmin):
    """
    Admin view for viewing affiliate sales history.
    """
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-history/', self.admin_site.admin_view(self.sales_history_view), name='sales_history'),
        ]
        return custom_urls + urls

    def sales_history_view(self, request):
        """Custom view to display affiliate sales history."""
        # Aggregate data
        sales_data = ProductPurchase.objects.filter(is_paid=True).values(
            'affiliate__user__username', 'product__name'
        ).annotate(
            total_sales=Count('id'),
            total_earnings=Sum('commission_earned'),
            total_amount=Sum('amount'),
        ).order_by('-total_sales')

        # Generate a response
        response = "<h1>Affiliate Sales History</h1><table border='1'>"
        response += "<tr><th>Affiliate</th><th>Product</th><th>Total Sales</th><th>Total Earnings</th><th>Total Amount</th></tr>"
        for data in sales_data:
            response += (
                f"<tr><td>{data['affiliate__user__username']}</td>"
                f"<td>{data['product__name']}</td>"
                f"<td>{data['total_sales']}</td>"
                f"<td>${data['total_earnings']}</td>"
                f"<td>${data['total_amount']}</td></tr>"
            )
        response += "</table>"

        return HttpResponse(response)

# Register the SalesHistoryAdminView in ProductPurchaseAdmin
class CustomProductPurchaseAdmin(ProductPurchaseAdmin, SalesHistoryAdminView):
    pass

admin.site.unregister(ProductPurchase)
admin.site.register(ProductPurchase, CustomProductPurchaseAdmin)
