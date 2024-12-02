from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from affiliates.models import Affiliate
from .models import CustomUser , UserProfile

class UserProfileForm(forms.ModelForm):
    """Form for creating and updating user profiles."""
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'address', 'city', 'state', 'country',
            'website_url', 'tax_identification_number', 'preferred_payment_method',
            'bank_account_details'
        ]


class AffiliateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    referred_by = forms.ModelChoiceField(
        queryset=Affiliate.objects.all(), required=False, widget=forms.HiddenInput()
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'referred_by']

    def __init__(self, *args, **kwargs):
        referrer = kwargs.pop('referrer', None)
        super().__init__(*args, **kwargs)
        if referrer:
            self.fields['referred_by'].initial = referrer
            self.fields['referred_by'].widget.attrs['readonly'] = True  # Make field non-editable

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')
