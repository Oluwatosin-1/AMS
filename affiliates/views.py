from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomLoginForm, CustomUserRegistrationForm, AffiliateProfileForm
from .models import CustomUser 
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

class CustomLogoutView(LogoutView):
    next_page = '/'


def register_user(request):
    if request.method == 'POST':
        user_form = CustomUserRegistrationForm(request.POST)
        profile_form = AffiliateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Assign additional profile details if needed
            if user.user_type == 'affiliate':
                # Process affiliate-specific data
                pass
            login(request, user)  # Automatically log in the user
            return redirect('dashboard')  # Redirect to an appropriate dashboard
    else:
        user_form = CustomUserRegistrationForm()
        profile_form = AffiliateProfileForm()
    return render(request, 'affiliates/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



class CustomLoginView(LoginView):
    template_name = 'affiliates/login.html'
    authentication_form = CustomLoginForm
    
    
@login_required
def affiliate_dashboard(request):
    # Add logic to display affiliate-specific data
    return render(request, 'affiliates/dashboard.html')

@login_required
def admin_dashboard(request):
    # Add logic to display admin-specific data
    return render(request, 'affiliates/admin_dashboard.html')
