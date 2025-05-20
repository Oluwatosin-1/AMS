from django import forms

from payments.models import PayoutRequest


class PayoutRequestForm(forms.ModelForm):
    class Meta:
        model = PayoutRequest
        fields = ["amount"]
