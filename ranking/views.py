from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from ranking.utils import update_affiliate_rank 
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

login_required
def view_rewards(request):
    """View to display affiliate rewards."""
    affiliate = request.user.affiliate
    rewards = AffiliateRank.objects.filter(affiliate=affiliate).select_related('current_rank')
    return render(request, 'affiliates/rewards.html', {'rewards': rewards})