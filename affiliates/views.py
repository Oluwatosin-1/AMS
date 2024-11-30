from django.shortcuts import render, redirect
from django.contrib.auth import login

from products.models import AffiliateProductLink, ProductPurchase
from training.models import TrainingModule
from .forms import AdminRegistrationForm, AffiliateRegistrationForm, AffiliateProfileForm 
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden  
from .models import  Affiliate

def register_user(request):
    referrer_id = request.GET.get('ref')  # Referral ID passed as a query parameter

    if request.method == 'POST':
        user_form = AffiliateRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'affiliate'
            user.save()

            referrer = Affiliate.objects.filter(user_id=referrer_id).first()
            Affiliate.objects.create(user=user, referred_by=referrer)  # Link referrer if exists

            login(request, user)  # Automatically log in the user
            return redirect('affiliate_dashboard')
    else:
        user_form = AffiliateRegistrationForm()
    return render(request, 'affiliates/register.html', {'user_form': user_form})


def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'admin'
            user.save()
            return redirect('admin_dashboard')
    else:
        form = AdminRegistrationForm()
    return render(request, 'affiliates/register_admin.html', {'form': form})

class CustomLogoutView(LogoutView):
    next_page = '/'
    
def role_based_redirect(get_response):
    def middleware(request):
        print(f"User authenticated: {request.user.is_authenticated}, Path: {request.path}")
        if request.user.is_authenticated:
            if request.path in [reverse('admin_dashboard'), reverse('affiliate_dashboard')]:
                return get_response(request)  # Prevent redirection loop

            if request.user.user_type == 'admin':
                print("Redirecting to admin dashboard")
                return redirect('admin_dashboard')
            elif request.user.user_type == 'affiliate':
                print("Redirecting to affiliate dashboard")
                return redirect('affiliate_dashboard')

        return get_response(request)
    return middleware

@login_required
def update_affiliate_profile(request):
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        form = AffiliateProfileForm(request.POST)
        if form.is_valid():
            profile_data = form.cleaned_data
            affiliate = request.user.affiliate
            affiliate.user.first_name = profile_data.get('full_name')
            affiliate.user.save()
            affiliate.phone_number = profile_data.get('phone_number')
            affiliate.address = profile_data.get('address')
            affiliate.city = profile_data.get('city')
            affiliate.state = profile_data.get('state')
            affiliate.country = profile_data.get('country')
            affiliate.website_url = profile_data.get('website_url')
            affiliate.tax_identification_number = profile_data.get('tax_identification_number')
            affiliate.preferred_payment_method = profile_data.get('preferred_payment_method')
            affiliate.bank_account_details = profile_data.get('bank_account_details')
            affiliate.save()
            return redirect('affiliate_dashboard')
    else:
        form = AffiliateProfileForm()

    return render(request, 'affiliates/update_profile.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'affiliates/login.html'

    def get_success_url(self):
        # Redirect based on user roles after login
        user = self.request.user
        if user.is_superuser:
            return reverse('admin:index')  # Django admin site
        elif user.user_type == 'admin':
            return reverse('admin_dashboard')
        elif user.user_type == 'affiliate':
            return reverse('affiliate_dashboard')
        return reverse('login')  # Default fallback
 
@login_required
def admin_dashboard(request):
    # Allow superusers and regular admins
    if request.user.user_type != 'admin' and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'affiliates/admin_dashboard.html')

@login_required
def affiliate_dashboard(request):
    # Restrict access to affiliates only
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")
    # Add affiliate-specific logic
    display_name = request.user.full_name if request.user.full_name else request.user.username

    return render(request, 'affiliates/dashboard.html', {'display_name': display_name})


@login_required
def affiliate_links(request):
    # Ensure only affiliates can access their links
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    links = AffiliateProductLink.objects.filter(affiliate__user=request.user)
    return render(request, 'affiliates/links.html', {'links': links})


@login_required
def affiliate_earnings(request):
    # Ensure only affiliates can view their earnings
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    earnings = ProductPurchase.objects.filter(affiliate__user=request.user)
    return render(request, 'affiliates/earnings.html', {'earnings': earnings})


@login_required
def affiliate_training(request):
    # Ensure only affiliates can access training
    if request.user.user_type != 'affiliate':
        return HttpResponseForbidden("You are not authorized to access this page.")

    training_modules = TrainingModule.objects.all()
    return render(request, 'training/modules.html', {'modules': training_modules})
