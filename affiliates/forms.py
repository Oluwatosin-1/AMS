from django import forms
from .models import Affiliate

class AffiliateProfileForm(forms.ModelForm):
    class Meta:
        model = Affiliate
        fields = ['commission_rate', 'training_completed', 'payout_threshold']
