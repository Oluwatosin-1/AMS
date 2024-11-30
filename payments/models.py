from django.db import models
from affiliates.models import Affiliate

class Payment(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment to {self.affiliate.user.username}: {self.amount}"
