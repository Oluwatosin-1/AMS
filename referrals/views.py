from django.shortcuts import render

from affiliates.models import Affiliate
from .models import Referral

def referral_list(request):
    referrals = Referral.objects.filter(affiliate=request.user.affiliate)
    return render(request, 'referrals/list.html', {'referrals': referrals})

def referral_tree(request):
    affiliates = Affiliate.objects.all()  # This assumes a hierarchy structure exists
    return render(request, 'referrals/tree.html', {'affiliates': affiliates})
