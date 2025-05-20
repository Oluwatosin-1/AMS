from django.db import models
from django.conf import settings
from decimal import Decimal


class Referral(models.Model):
    affiliate = models.ForeignKey("affiliates.Affiliate", on_delete=models.CASCADE)
    referred_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, null=True, blank=True
    )
    client_email = models.EmailField()
    referred_at = models.DateTimeField(auto_now_add=True)
    commission_earned = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )

    def save(self, *args, **kwargs):
        """
        Automatically calculate commission only for valid referral types.
        """
        if self.referred_user and not self.product:
            # Referral bonus for user registration
            self.commission_earned = Decimal(10.00)  # Example flat rate commission
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.affiliate.user.username} referred {self.client_email}"
