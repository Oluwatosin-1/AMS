from django.contrib import admin
from .models import Rank, AffiliateRank

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['title', 'min_personal_referrals', 'min_total_referrals', 'reward', 'is_active']
    search_fields = ['title']
    list_filter = ['is_active']

@admin.register(AffiliateRank)
class AffiliateRankAdmin(admin.ModelAdmin):
    list_display = ['affiliate', 'current_rank', 'achieved_at']
    search_fields = ['affiliate__user__username', 'current_rank__title']
    list_filter = ['current_rank']
