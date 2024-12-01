from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator 
from django.db.models import Sum
from ranking.utils import update_affiliate_rank
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
        current_rank = affiliate.rank.current_rank if hasattr(affiliate, 'rank') else None

        # Add additional context variables
        context.update({
            'display_name': self.request.user.full_name or self.request.user.username, 
            'rank': current_rank.title if current_rank else "No Rank",
            'rank_logo': current_rank.logo.url if current_rank and current_rank.logo else None,
            'rank_reward': current_rank.reward if current_rank else 0,    
            'referrals': Affiliate.objects.filter(referred_by=affiliate),  # Downline tracking
            'links': AffiliateProductLink.objects.filter(affiliate=affiliate),  # Affiliate links
            'link_clicks': AffiliateProductLink.objects.filter(affiliate=affiliate).aggregate(
                total_clicks=Sum('clicks')
            )['total_clicks'] or 0,
            'total_earnings': ProductPurchase.objects.filter(affiliate=affiliate).aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'total_products_sold': ProductPurchase.objects.filter(affiliate=affiliate).count(),
            'training_modules': TrainingModule.objects.all(),  # Add training modules if available
            'year': now().year,  # Current year
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
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    earnings = ProductPurchase.objects.filter(affiliate__user=request.user)
    total_earnings = sum(purchase.amount for purchase in earnings)
    
    return render(request, 'affiliates/earnings.html', {'earnings': earnings, 'total_earnings': total_earnings})

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
