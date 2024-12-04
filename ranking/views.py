from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Sum
from products.models import ProductPurchase
from ranking.utils import update_affiliate_rank
from referrals.models import Referral 
from .models import Rank, AffiliateRank 

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

@login_required
def view_rewards(request):
    """View to display affiliate rewards and additional details."""
    affiliate = request.user.affiliate

    # Fetch rewards and related data
    rewards = AffiliateRank.objects.filter(affiliate=affiliate).select_related('current_rank')

    # Calculate total earnings breakdown
    product_commissions = ProductPurchase.objects.filter(affiliate=affiliate).aggregate(
        total=Sum('commission_earned')
    )['total'] or 0

    referral_commissions = Referral.objects.filter(affiliate=affiliate).aggregate(
        total=Sum('commission_earned')
    )['total'] or 0

    rank_rewards = sum(reward.current_rank.reward for reward in rewards if reward.current_rank)
    total_earnings = product_commissions + referral_commissions + rank_rewards

    return render(
        request,
        'affiliates/rewards.html',
        {
            'rewards': rewards,
            'product_commissions': product_commissions,
            'referral_commissions': referral_commissions,
            'rank_rewards': rank_rewards,
            'total_earnings': total_earnings,
        },
    )
