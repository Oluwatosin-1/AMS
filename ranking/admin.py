from django.contrib import admin
from .models import Rank, AffiliateRank


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    """
    Admin configuration for Rank model.
    """
    list_display = (
        'title',
        'min_personal_referrals',
        'min_total_referrals',
        'reward',
        'personal_referral_commission',
        'initial_level_commission',
        'renewal_level_commission',
        'is_active',
    )
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    readonly_fields = ('id',)

    fieldsets = (
        ("Basic Information", {
            'fields': ('title', 'description', 'logo', 'node_color')
        }),
        ("Rank Rules", {
            'fields': ('min_personal_referrals', 'min_total_referrals')
        }),
        ("Rank Rewards and Commissions", {
            'fields': ('reward', 'personal_referral_commission', 'initial_level_commission', 'renewal_level_commission')
        }),
        ("Additional Information", {
            'fields': ('admin_note', 'is_active')
        }),
    )


@admin.register(AffiliateRank)
class AffiliateRankAdmin(admin.ModelAdmin):
    """
    Admin configuration for AffiliateRank model.
    """
    list_display = (
        'affiliate_username',
        'current_rank_title',
        'achieved_at',
    )
    list_filter = ('current_rank', 'achieved_at')
    search_fields = ('affiliate__user__username', 'current_rank__title')
    readonly_fields = ('achieved_at',)

    def affiliate_username(self, obj):
        """
        Display the affiliate's username.
        """
        return obj.affiliate.user.username
    affiliate_username.short_description = "Affiliate Username"

    def current_rank_title(self, obj):
        """
        Display the current rank's title.
        """
        return obj.current_rank.title if obj.current_rank else "No Rank"
    current_rank_title.short_description = "Current Rank"
