from django.shortcuts import render

from affiliates.models import Affiliate
from .models import Referral 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def view_referrals(request):
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    referrals = Affiliate.objects.filter(referred_by=affiliate)

    return render(request, 'affiliates/referrals.html', {'referrals': referrals})

def referral_list(request):
    referrals = Referral.objects.filter(affiliate=request.user.affiliate)
    return render(request, 'referrals/list.html', {'referrals': referrals})

@login_required
def referral_tree(request):
    """View for displaying the referral tree."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    downline = Affiliate.objects.filter(referred_by=affiliate)

    # Format for tree visualization
    referral_tree = [
        {
            'name': child.user.full_name or child.user.username,
            'rank': child.rank.current_rank.title if hasattr(child, 'rank') and child.rank.current_rank else "No Rank",
            'referrals': child.referrals
        }
        for child in downline
    ]

    return render(request, 'affiliates/referral_tree.html', {'referral_tree': referral_tree})
