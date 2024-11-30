from django.contrib import admin
from .models import Product, AffiliateProductLink, ProductPurchase

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('created_at',)

@admin.register(AffiliateProductLink)
class AffiliateProductLinkAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'product', 'unique_url', 'clicks')
    search_fields = ('affiliate__user__username', 'product__name')
    ordering = ('affiliate',)

@admin.register(ProductPurchase)
class ProductPurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'affiliate', 'client_email', 'amount', 'purchased_at')
    list_filter = ('purchased_at',)
    search_fields = ('product__name', 'client_email')
    ordering = ('purchased_at',)
