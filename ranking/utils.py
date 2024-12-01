from django.utils.timezone import now
from .models import Rank, AffiliateRank

def update_affiliate_rank(affiliate):
    """Update the rank of an affiliate based on referral statistics."""
    total_referrals = affiliate.referrals_downline.count()
    personal_referrals = affiliate.referrals

    # Find the highest eligible rank
    eligible_ranks = Rank.objects.filter(
        min_personal_referrals__lte=personal_referrals,
        min_total_referrals__lte=total_referrals,
        is_active=True
    ).order_by('-min_personal_referrals', '-min_total_referrals')  # Higher ranks first

    if eligible_ranks.exists():
        new_rank = eligible_ranks.first()
        affiliate_rank, created = AffiliateRank.objects.get_or_create(affiliate=affiliate)
        if affiliate_rank.current_rank != new_rank:
            affiliate_rank.current_rank = new_rank
            affiliate_rank.achieved_at = now()
            affiliate_rank.save()

