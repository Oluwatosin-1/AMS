from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator 
from django.db.models import Sum
from ranking.models import Rank
from ranking.utils import update_affiliate_rank
from referrals.models import Referral
from training.models import TrainingModule
from .models import Affiliate
from products.models import AffiliateProductLink, Product, ProductPurchase
from .forms import AffiliateProfileForm
from django.utils.timezone import now  # For the current year 
from django.conf import settings  # To fetch site domain dynamically 

@method_decorator(login_required, name='dispatch')
class RoleBasedDashboardView(TemplateView):
    """Redirect users to their respective dashboards based on role."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type == 'admin':
            return redirect('admin_dashboard')
        elif request.user.user_type == 'affiliate':
            return redirect('affiliate_dashboard')
        return super().dispatch(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class AffiliateDashboardView(ListView):
    """Affiliate-specific dashboard."""
    model = ProductPurchase
    template_name = "users/dashboard.html"

    def get_queryset(self):
        """Fetch all product purchases associated with the affiliate."""
        return ProductPurchase.objects.filter(affiliate__user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add context data for dashboard metrics and related data."""
        context = super().get_context_data(**kwargs)
        affiliate = self.request.user.affiliate

        # Update the affiliate's rank
        update_affiliate_rank(affiliate)

        # Current rank details
        current_rank = affiliate.rank.current_rank if hasattr(affiliate, 'rank') else None
        rank_rewards = current_rank.reward if current_rank else 0

        # Immediate personal referrals
        personal_referrals = Affiliate.objects.filter(referred_by=affiliate).count()

        # Total referrals including downline (recursive relationships)
        total_referrals = Affiliate.objects.filter(
            referred_by__in=Affiliate.objects.filter(referred_by=affiliate)
        ).count() + personal_referrals

        # Next rank details
        next_rank = (
            Rank.objects.filter(
                is_active=True,
                min_personal_referrals__gt=(current_rank.min_personal_referrals if current_rank else 0),
            )
            .order_by('min_personal_referrals', 'min_total_referrals')
            .first()
        )

        # Calculate earnings
        product_commissions = ProductPurchase.objects.filter(affiliate=affiliate).aggregate(
            total=Sum('commission_earned')
        )['total'] or 0

        referral_commissions = Referral.objects.filter(affiliate=affiliate).aggregate(
            total=Sum('commission_earned')
        )['total'] or 0

        total_earnings = product_commissions + referral_commissions + rank_rewards

        # Wallet balance (considering payouts) 
        total_withdrawn = affiliate.payouts.aggregate(total=Sum('amount'))['total'] or 0
        wallet_balance = total_earnings - total_withdrawn
        # Conversion rate calculation
        total_clicks = AffiliateProductLink.objects.filter(affiliate=affiliate).aggregate(
            total_clicks=Sum('clicks')
        )['total_clicks'] or 0

        conversions = ProductPurchase.objects.filter(affiliate=affiliate).count()
        conversion_rate = (conversions / total_clicks * 100) if total_clicks > 0 else 0

        # Sponsor details
        sponsor = affiliate.referred_by

        # Recent referrals
        recent_referrals = Affiliate.objects.filter(referred_by=affiliate).order_by('-created_at')[:5]

        # Add context variables
        context.update({
            'display_name': self.request.user.full_name or self.request.user.username,
            'rank': current_rank.title if current_rank else "No Rank",
            'rank_logo': current_rank.logo.url if current_rank and current_rank.logo else None,
            'rank_reward': rank_rewards,
            'next_rank': next_rank.title if next_rank else "No further ranks available",
            'next_rank_min_personal_referrals': next_rank.min_personal_referrals if next_rank else None,
            'next_rank_min_total_referrals': next_rank.min_total_referrals if next_rank else None,
            'product_commissions': product_commissions,
            'referral_commissions': referral_commissions,
            'total_earnings': total_earnings,
            'wallet_balance': wallet_balance,
            'total_products_sold': ProductPurchase.objects.filter(affiliate=affiliate).count(),
            'referrals': Affiliate.objects.filter(referred_by=affiliate),  # Downline tracking
            'personal_referrals': personal_referrals,
            'total_referrals': total_referrals,
            'affiliate_products': Product.objects.filter(affiliateproductlink__affiliate=affiliate),
            'training_modules': TrainingModule.objects.all(),
            'total_clicks': total_clicks,
            'conversion_rate': conversion_rate,
            'register_date': affiliate.created_at,
            'sponsor_name': sponsor.user.full_name if sponsor else "No Sponsor",
            'sponsor_email': sponsor.user.email if sponsor else "N/A",
            'sponsor_phone': sponsor.phone if sponsor and hasattr(sponsor, 'phone') else "N/A",
            'sponsor_location': sponsor.location if sponsor and hasattr(sponsor, 'location') else "N/A",
            'recent_referrals': recent_referrals,
            'performance_chart_labels': ['Jan', 'Feb', 'Mar', 'Apr'],  # Replace with actual data
            'performance_chart_referrals': [10, 20, 15, 30],
            'performance_chart_products': [5, 8, 10, 12],
            'performance_chart_clicks': [50, 70, 90, 110],
            'year': now().year,
        })

        return context

@method_decorator(login_required, name='dispatch')
class AdminDashboardView(ListView):
    """Admin-specific dashboard."""
    model = Affiliate
    template_name = "users/admin_dashboard.html"

    def get_queryset(self):
        return Affiliate.objects.all()

@login_required
def update_affiliate_profile(request):
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    if request.method == 'POST':
        form = AffiliateProfileForm(request.POST, instance=affiliate)
        if form.is_valid():
            form.save()
            return redirect('affiliate_dashboard')
    else:
        form = AffiliateProfileForm(instance=affiliate)
    
    return render(request, 'users/update_profile.html', {'form': form})

@login_required
def affiliate_earnings(request):
    affiliate = request.user.affiliate

    # Calculate earnings
    referral_earnings = Referral.objects.filter(
        affiliate=affiliate, referred_user__isnull=False
    ).aggregate(total=Sum('commission_earned'))['total'] or 0

    product_earnings = ProductPurchase.objects.filter(
        affiliate=affiliate
    ).aggregate(total=Sum('commission_earned'))['total'] or 0

    rank_reward = affiliate.rank.current_rank.reward if affiliate.rank.current_rank else 0
    total_earnings = referral_earnings + product_earnings + rank_reward

    # Fetch individual entries for breakdown
    referrals = Referral.objects.filter(affiliate=affiliate, referred_user__isnull=False)
    product_purchases = ProductPurchase.objects.filter(affiliate=affiliate)

    return render(request, 'affiliates/earnings.html', {
        'total_product_earnings': product_earnings,
        'total_referral_earnings': referral_earnings,
        'rank_reward': rank_reward,
        'total_earnings': total_earnings,
        'referrals': referrals,
        'product_purchases': product_purchases,
    })

@login_required
def affiliate_training(request):
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    training_modules = TrainingModule.objects.all()
    return render(request, 'trainings/modules.html', {'modules': training_modules})

@login_required
def list_affiliate_links(request):
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    links = AffiliateProductLink.objects.filter(affiliate=affiliate)

    products_without_links = Product.objects.exclude(
        id__in=links.values_list('product_id', flat=True)
    )

    return render(request, 'affiliates/affiliate_links.html', {
        'links': links,
        'products_without_links': products_without_links,
    })
    

@login_required
def generate_referral_link(request):
    """Generate a referral link for the affiliate."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    affiliate = request.user.affiliate
    referral_path = reverse('register_user')  # URL pattern for registration
    referral_link = f"{settings.SITE_DOMAIN}{referral_path}?ref={affiliate.id}"  # Full URL with domain
    print(f"Generated Referral Link: {referral_link}")  # Debug log
    return render(request, 'affiliates/referral_link.html', {'referral_link': referral_link})

@login_required
def view_downline(request):
    """View for tracking downline affiliates."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    affiliate = request.user.affiliate
    referrals = Affiliate.objects.filter(referred_by=affiliate)

    # Preprocess referrals for cleaner template
    referrals_with_details = [
        {
            'name': referral.user.full_name or referral.user.username,
            'email': referral.user.email,
            'join_date': referral.created_at,
            'referrals_made': referral.referrals
        }
        for referral in referrals
    ]

    return render(request, 'affiliates/downline.html', {'referrals': referrals_with_details})

@login_required
def delete_affiliate(request, pk):
    """Admin-specific action to delete an affiliate."""
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    affiliate = get_object_or_404(Affiliate, pk=pk)
    if request.method == 'POST':
        affiliate.delete()
        return redirect('admin_dashboard')
    return render(request, 'affiliates/confirm_delete.html', {'affiliate': affiliate})

