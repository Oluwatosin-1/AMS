from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from affiliates.models import Affiliate
from .models import Rank, AffiliateRank
from django.utils.timezone import now


def update_affiliate_rank(affiliate):
    """Update the rank of an affiliate based on referral statistics."""
    total_referrals = Affiliate.objects.filter(referred_by=affiliate).count()
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
            print(f"Updated rank to {new_rank.title} for {affiliate.user.username}")


@login_required
def rank_list(request):
    """Admin view to manage ranks."""
    if not request.user.is_staff:
        return HttpResponseForbidden("Only admins can manage ranks.")

    ranks = Rank.objects.all()
    return render(request, 'ranking/rank_list.html', {'ranks': ranks})


@login_required
def affiliate_rank(request):
    """View for affiliates to see their current rank."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("Only affiliates can view their rank.")

    affiliate = request.user.affiliate
    update_affiliate_rank(affiliate)
    affiliate_rank = affiliate.rank.current_rank if hasattr(affiliate, 'rank') else None

    return render(request, 'ranking/affiliate_rank.html', {'rank': affiliate_rank})

login_required
def view_rewards(request):
    """View to display affiliate rewards."""
    affiliate = request.user.affiliate
    rewards = AffiliateRank.objects.filter(affiliate=affiliate).select_related('current_rank')
    return render(request, 'affiliates/rewards.html', {'rewards': rewards})