from django.db import models
from affiliates.models import Affiliate
class Referral(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    client_email = models.EmailField()
    referred_at = models.DateTimeField(auto_now_add=True)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.affiliate.user.username} - {self.product.name}"
