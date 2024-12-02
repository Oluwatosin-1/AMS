from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from users.models import CustomUser, UserProfile
from .forms import AffiliateRegistrationForm, AdminRegistrationForm, UserProfileForm
from affiliates.models import Affiliate 
from django.contrib.auth import logout
from django.contrib import messages
# Create your views here.

def home(request):
    """Display the home page."""
    return render(request, 'index2.html')

def register_user(request):
    """Register a new user and handle referrals."""
    referrer = None

    # Capture referral ID from query parameters
    ref = request.GET.get('ref')
    if ref:
        referrer = Affiliate.objects.filter(id=ref).first()
    else:
        # Default to the first admin as referrer
        admin_user = CustomUser.objects.filter(user_type='admin').first()
        if admin_user:
            referrer = Affiliate.objects.filter(user=admin_user).first()

    if request.method == 'POST':
        user_form = AffiliateRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create user
            user = user_form.save(commit=False)
            user.user_type = 'affiliate'
            user.full_name = f"{user_form.cleaned_data['first_name']} {user_form.cleaned_data['last_name']}"
            user.save()
            # Create affiliate profile and link referrer
            affiliate = Affiliate.objects.create(user=user, referred_by=referrer)

            # Update referrer's referrals
            if referrer:
                referrer.increase_referrals()

            login(request, user)  # Log in the user
            return redirect('affiliate_dashboard')
    else:
        user_form = AffiliateRegistrationForm()

    return render(request, 'users/register.html', {'user_form': user_form, 'referrer': referrer})

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
    return render(request, 'users/register_admin.html', {'form': form})

def custom_logout(request):
    """Handle custom logout."""
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out successfully.")  # Optional success message
    return redirect('login')  # Redirect to the login page


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
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
def view_profile(request):
    """View the logged-in user's profile."""
    try:
        profile = request.user.profile  # Access the related UserProfile
    except UserProfile.DoesNotExist:
        # Redirect to create profile if it doesn't exist
        return redirect('create_profile')

    return render(request, 'users/view_profile.html', {'profile': profile})

@login_required
def create_profile(request):
    """Create a profile for the logged-in user."""
    if hasattr(request.user, 'profile'):
        # Redirect to update profile if it already exists
        return redirect('update_profile')

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm()

    return render(request, 'users/create_profile.html', {'form': form})

@login_required
def update_profile(request):
    """Update the logged-in user's profile."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Redirect to create profile if it doesn't exist
        return redirect('create_profile')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'users/update_profile.html', {'form': form})