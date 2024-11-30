from django.db import models
from affiliates.models import Affiliate

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AffiliateProductLink(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unique_url = models.URLField(unique=True)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.affiliate.user.username} - {self.product.name}"

class ProductPurchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.SET_NULL, null=True, blank=True)
    client_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} by {self.client_email}"
