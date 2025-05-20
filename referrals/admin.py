from django.contrib import admin
from .models import Referral


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Referral model.
    """

    list_display = (
        "affiliate_username",
        "client_email",
        "referred_user_username",
        "product_name",
        "commission_earned",
        "referred_at",
    )
    list_filter = ("referred_at", "affiliate")
    search_fields = (
        "affiliate__user__username",
        "client_email",
        "referred_user__username",
        "product__name",
    )
    readonly_fields = ("referred_at", "commission_earned")

    def affiliate_username(self, obj):
        """
        Display the username of the affiliate who made the referral.
        """
        return obj.affiliate.user.username

    affiliate_username.short_description = "Affiliate Username"

    def referred_user_username(self, obj):
        """
        Display the username of the referred user, if applicable.
        """
        return obj.referred_user.username if obj.referred_user else "N/A"

    referred_user_username.short_description = "Referred User"

    def product_name(self, obj):
        """
        Display the name of the referred product, if applicable.
        """
        return obj.product.name if obj.product else "N/A"

    product_name.short_description = "Product"
