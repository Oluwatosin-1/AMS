from django.contrib import admin
from .models import Affiliate, AffiliateEarning


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Affiliate model.
    """

    list_display = (
        "user",
        "get_rank_title",
        "commission_rate",
        "referrals",
        "training_completed",
        "calculate_total_earnings",
        "payout_threshold",
        "created_at",
    )
    list_filter = ("training_completed", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = (
        "calculate_total_earnings",
        "get_rank_title",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Affiliate Details",
            {
                "fields": (
                    "user",
                    "referred_by",
                    "commission_rate",
                    "training_completed",
                    "payout_threshold",
                )
            },
        ),
        (
            "Affiliate Statistics",
            {"fields": ("referrals", "get_rank_title", "calculate_total_earnings")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def calculate_total_earnings(self, obj):
        return f"${obj.calculate_total_earnings():,.2f}"

    calculate_total_earnings.short_description = "Total Earnings"

    def get_rank_title(self, obj):
        return obj.get_rank_title()

    get_rank_title.short_description = "Rank"


@admin.register(AffiliateEarning)
class AffiliateEarningAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AffiliateEarning model.
    """

    list_display = ("affiliate", "earning_type", "amount", "description", "created_at")
    list_filter = ("earning_type", "created_at")
    search_fields = (
        "affiliate__user__username",
        "affiliate__user__email",
        "description",
    )
    date_hierarchy = "created_at"
    fields = ("affiliate", "earning_type", "amount", "description", "created_at")
    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        """
        Override the queryset to annotate total earnings for affiliates in the list view.
        """
        qs = super().get_queryset(request)
        return qs.select_related("affiliate")
