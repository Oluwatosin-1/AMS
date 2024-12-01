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

def referral_tree(request):
    affiliates = Affiliate.objects.all()  # This assumes a hierarchy structure exists
    return render(request, 'referrals/tree.html', {'affiliates': affiliates})
