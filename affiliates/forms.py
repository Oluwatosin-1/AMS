from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import CustomUser

class AffiliateRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # No user_type field

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # No user_type field

class AffiliateProfileForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    website_url = forms.URLField(required=False)
    tax_identification_number = forms.CharField(max_length=50, required=False)
    preferred_payment_method = forms.ChoiceField(
        choices=[('paypal', 'PayPal'), ('bank_transfer', 'Bank Transfer')],
        widget=forms.RadioSelect
    )
    bank_account_details = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("preferred_payment_method")
        if payment_method == 'bank_transfer' and not cleaned_data.get("bank_account_details"):
            self.add_error('bank_account_details', "Bank account details are required for bank transfer.")

class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.", code='inactive',
            )
