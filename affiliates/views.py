from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator 
from django.db.models import Sum
from ranking.models import Rank
from ranking.utils import get_affiliate_performance_data, update_affiliate_rank
from referrals.models import Referral
from training.models import TrainingModule, TrainingProgress
from .models import Affiliate
from products.models import AffiliateProductLink, Product, ProductPurchase
from .forms import AffiliateProfileForm
from django.utils.timezone import now  # For the current year 
from django.conf import settings  # To fetch site domain dynamically  
from django.http import JsonResponse

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
        
        # Performance data (example logic)
        performance_data = get_affiliate_performance_data(affiliate)

        # Recent referrals
        recent_referrals = Affiliate.objects.filter(referred_by=affiliate).order_by('-created_at')[:5]
         # Default referral link
        referral_path = reverse('register_user')
        default_referral_link = f"{settings.SITE_DOMAIN}{referral_path}?ref={affiliate.id}"

        # Product-specific referral links
        product_links = AffiliateProductLink.objects.filter(affiliate=affiliate)

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
            'sponsor_phone': sponsor.user.profile.phone_number if sponsor and hasattr(sponsor.user, 'profile') else "N/A",
            'sponsor_location': f"{sponsor.user.profile.city}, {sponsor.user.profile.state}, {sponsor.user.profile.country}" 
                if sponsor and hasattr(sponsor.user, 'profile') else "N/A", 
            'user_phone': affiliate.user.profile.phone_number if hasattr(affiliate.user, 'profile') else "N/A",
            'user_location': f"{affiliate.user.profile.city}, {affiliate.user.profile.state}, {affiliate.user.profile.country}" 
                if hasattr(affiliate.user, 'profile') else "N/A",
            'recent_referrals': recent_referrals,
            'performance_chart_labels': performance_data['chart_labels'],
            'performance_chart_products': performance_data['chart_sales'],
            'performance_chart_commissions': performance_data['chart_commissions'],
            'product_links': product_links,  # Add product-specific referral links
            'default_referral_link': default_referral_link,
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
    """Display affiliate earnings with wallet and payout options."""
    affiliate = request.user.affiliate

    # Calculate earnings
    referral_earnings = Referral.objects.filter(
        affiliate=affiliate, referred_user__isnull=False
    ).aggregate(total=Sum('commission_earned'))['total'] or 0

    product_earnings = ProductPurchase.objects.filter(
        affiliate=affiliate
    ).aggregate(total=Sum('commission_earned'))['total'] or 0

    rank_reward = (
        affiliate.rank.current_rank.reward
        if hasattr(affiliate, 'rank') and affiliate.rank.current_rank
        else 0
    )
    total_earnings = referral_earnings + product_earnings + rank_reward

    # Calculate wallet balance
    total_withdrawn = affiliate.payouts.aggregate(total=Sum('amount'))['total'] or 0
    wallet_balance = total_earnings - total_withdrawn

    # Check eligibility for payout and calculate remaining amount to threshold
    payout_threshold = affiliate.payout_threshold
    remaining_to_threshold = max(0, payout_threshold - wallet_balance)
    eligible_for_payout = wallet_balance >= payout_threshold

    # Fetch individual entries for breakdown
    referrals = Referral.objects.filter(affiliate=affiliate, referred_user__isnull=False)
    product_purchases = ProductPurchase.objects.filter(affiliate=affiliate)

    return render(request, 'affiliates/earnings.html', {
        'total_product_earnings': product_earnings,
        'total_referral_earnings': referral_earnings,
        'rank_reward': rank_reward,
        'total_earnings': total_earnings,
        'wallet_balance': wallet_balance,
        'payout_threshold': payout_threshold,
        'remaining_to_threshold': remaining_to_threshold,
        'eligible_for_payout': eligible_for_payout,
        'referrals': referrals,
        'product_purchases': product_purchases,
    })
     
@login_required
def affiliate_training(request):
    """
    Display available training modules with progress status.
    Fetches all training modules and categorizes them by status: not started, in progress, and completed.
    """
    modules = TrainingModule.objects.all()
    progress_list = TrainingProgress.objects.filter(user=request.user)
    progress_mapping = {progress.module.id: progress for progress in progress_list}

    categorized_modules = {
        'not_started': [],
        'in_progress': [],
        'completed': [],
    }

    for module in modules:
        progress = progress_mapping.get(module.id)
        if not progress:
            categorized_modules['not_started'].append(module)
        elif progress.completed:
            categorized_modules['completed'].append((module, progress))
        else:
            categorized_modules['in_progress'].append((module, progress))

    context = {
        'categorized_modules': categorized_modules,
    }
    return render(request, 'trainings/modules.html', context)

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
    """Generate a referral link for the affiliate and display referrals."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    affiliate = request.user.affiliate
    referral_path = reverse('register_user')  # URL pattern for registration
    referral_link = f"{settings.SITE_DOMAIN}{referral_path}?ref={affiliate.id}"  # Full URL with domain
    
    # Fetch referrals
    referrals = Affiliate.objects.filter(referred_by=affiliate).values(
        'user__full_name', 'user__email', 'created_at', 'referrals'
    )
    referrals_with_details = [
        {
            'name': referral['user__full_name'] or 'No Name',
            'email': referral['user__email'],
            'join_date': referral['created_at'],
            'referrals_made': referral['referrals']
        }
        for referral in referrals
    ]

    return render(
        request,
        'affiliates/referral_list.html',
        {
            'referral_link': referral_link,
            'referrals': referrals_with_details,
        }
    )

@login_required
def view_genealogy(request):
    """View for tracking genealogy downline affiliates."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    referrals = Affiliate.objects.filter(referred_by=affiliate).select_related('rank__current_rank')

    # Preprocess data for the template
    genealogy = [
        {
            'name': referral.user.full_name or referral.user.username,
            'email': referral.user.email,
            'rank': referral.rank.current_rank.title if hasattr(referral, 'rank') and referral.rank.current_rank else "No Rank",
            'referrals': referral.referrals,
            'join_date': referral.created_at,
        }
        for referral in referrals
    ]

    ranks = Rank.objects.filter(is_active=True).order_by('min_personal_referrals')

    return render(request, 'affiliates/genealogy.html', {'genealogy': genealogy, 'ranks': ranks})

@login_required
def filter_genealogy_by_rank(request, rank_id):
    """Filter downline by rank."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate
    rank = get_object_or_404(Rank, id=rank_id)

    referrals = Affiliate.objects.filter(referred_by=affiliate, rank__current_rank=rank)

    genealogy = [
        {
            'name': referral.user.full_name or referral.user.username,
            'email': referral.user.email,
            'rank': rank.title,
            'referrals': referral.referrals,
            'join_date': referral.created_at,
        }
        for referral in referrals
    ]

    ranks = Rank.objects.filter(is_active=True).order_by('min_personal_referrals')

    return render(request, 'affiliates/genealogy.html', {'genealogy': genealogy, 'ranks': ranks})

@login_required
def reset_genealogy(request):
    return redirect('view_genealogy')

@login_required
def genealogy_tree_data(request):
    """Provide JSON data for genealogy organogram."""
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    affiliate = request.user.affiliate

    def build_tree(affiliate, level=0):
        """Recursive function to build the genealogy tree."""
        children = Affiliate.objects.filter(referred_by=affiliate)
        color_class = "top-node" if level == 0 else "direct-referral-node" if level == 1 else "other-referral-node"

        return [
            {
                'text': {
                    'name': child.user.full_name or child.user.username,
                    'desc': f"Rank: {child.rank.current_rank.title if hasattr(child, 'rank') and child.rank.current_rank else 'No Rank'}",
                    'email': f"Email: {child.user.email}",
                },
                'HTMLclass': color_class,
                'children': build_tree(child, level + 1),
            }
            for child in children
        ]

    tree_data = {
        'text': {
            'name': affiliate.user.full_name or affiliate.user.username,
            'desc': f"Rank: {affiliate.rank.current_rank.title if hasattr(affiliate, 'rank') and affiliate.rank.current_rank else 'No Rank'}",
            'email': f"Email: {affiliate.user.email}",
        },
        'HTMLclass': "top-node",
        'children': build_tree(affiliate),
    }

    return JsonResponse(tree_data)

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

