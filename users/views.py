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
from django.db import transaction

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

# Create your views here.


def home(request):
    """Display the home page."""
    return render(request, "users/login.html")


def register_user(request):
    """Register a new user and handle referrals."""
    referrer = None

    ref = request.GET.get("ref")
    if ref:
        referrer = Affiliate.objects.filter(id=ref).first()
    else:
        # Default to the first admin as referrer
        admin_user = CustomUser.objects.filter(user_type="admin").first()
        if admin_user:
            referrer = Affiliate.objects.filter(user=admin_user).first()

    if request.method == "POST":
        user_form = AffiliateRegistrationForm(request.POST)
        if user_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                user.user_type = "affiliate"
                user.full_name = f"{user_form.cleaned_data['first_name']} {user_form.cleaned_data['last_name']}"
                user.save()
                print(f"User Created: {user.username}, {user.full_name}, {user.email}")

                affiliate = Affiliate.objects.create(user=user, referred_by=referrer)
                print(
                    f"Affiliate Created: {affiliate.user.username}, Referred By: {referrer}"
                )

                # Populate the user profile
                profile = user.profile
                profile.phone_number = user_form.cleaned_data["phone_number"]
                profile.address = user_form.cleaned_data["address"]
                profile.city = user_form.cleaned_data["city"]
                profile.state = user_form.cleaned_data["state"]
                profile.country = user_form.cleaned_data["country"]
                profile.save()
                print(f"UserProfile Updated: {profile.phone_number}, {profile.address}")

                if referrer:
                    # Increase referrer’s referral count
                    referrer.increase_referrals()
                    # **Changed total_referrals -> referrals**
                    print(
                        f"Referrer Updated: {referrer.user.username}, Total Referrals: {referrer.referrals}"
                    )

                login(request, user)
                return redirect("affiliate_dashboard")
        else:
            print(f"Form Errors: {user_form.errors}")
    else:
        user_form = AffiliateRegistrationForm()

    return render(
        request,
        "users/register.html",
        {"user_form": user_form, "referrer": referrer, "form_errors": user_form.errors},
    )


def register_admin(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = "admin"
            user.save()
            return redirect("admin_dashboard")
    else:
        form = AdminRegistrationForm()
    return render(request, "users/register_admin.html", {"form": form})


def custom_logout(request):
    """Handle custom logout."""
    logout(request)  # Log the user out
    messages.success(
        request, "You have been logged out successfully."
    )  # Optional success message
    return redirect("login")  # Redirect to the login page


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        # Redirect based on user roles after login
        user = self.request.user
        if user.is_superuser:
            return reverse("admin:index")  # Django admin site
        elif user.user_type == "admin":
            return reverse("admin_dashboard")
        elif user.user_type == "affiliate":
            return reverse("affiliate_dashboard")
        return reverse("login")  # Default fallback


@login_required
def view_profile(request):
    """View the logged-in user's profile."""
    try:
        profile = request.user.profile  # Access the related UserProfile
    except UserProfile.DoesNotExist:
        # Redirect to create profile if it doesn't exist
        return redirect("create_profile")

    return render(request, "users/view_profile.html", {"profile": profile})


@login_required
def create_profile(request):
    """Create a profile for the logged-in user."""
    if hasattr(request.user, "profile"):
        # Redirect to update profile if it already exists
        return redirect("update_profile")

    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("view_profile")
    else:
        form = UserProfileForm()

    return render(
        request,
        "users/create_profile.html",
        {
            "form": form,
            "form_title": "Create Your Profile",
            "submit_button_text": "Create Profile",
        },
    )


@login_required
def update_profile(request):
    """Update the logged-in user's profile."""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Redirect to create profile if it doesn't exist
        return redirect("create_profile")

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("view_profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(
        request,
        "users/update_profile.html",
        {
            "form": form,
            "form_title": "Update Your Profile",
            "submit_button_text": "Update Profile",
        },
    )


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
