from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from affiliates.models import Affiliate
from .models import CustomUser , UserProfile
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'address',
            'city',
            'state',
            'country',
            'website_url',
            'tax_identification_number',
            'preferred_payment_method',
            'bank_account_details',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'bank_account_details': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'needs-validation'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                Column('website_url', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('address', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('country', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('tax_identification_number', css_class='form-group col-md-6 mb-0'),
                Column('preferred_payment_method', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('bank_account_details', css_class='form-group col-md-12 mb-4'),
            ),
            Submit('submit', 'Save Profile', css_class='btn btn-primary btn-block mt-3')
        )

class AffiliateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        # Just create/save the User object
        user = super().save(commit=commit)
        return user
        
class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')
