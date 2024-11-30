from django.db import models
from affiliates.models import Affiliate


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('e-commerce', 'E-Commerce'),
        ('cms', 'CMS'),
        ('legal', 'Legal'),
        ('education', 'Education'),
        ('others', 'Others'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Default Price")
    default_commission = models.CharField(
        max_length=50,
        verbose_name="Default Commission",
        help_text="Comma-separated commission percentages, e.g., 5%, 2%"
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    sales_note = models.TextField(null=True, blank=True, help_text="Noted when sales occur")
    status = models.BooleanField(default=True, verbose_name="Active Status")
    keywords = models.TextField(help_text="Keywords to describe the product for search optimization")
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_commission_rates(self):
        """
        Returns the default commission rates as a list of floats.
        """
        try:
            return [float(rate.strip('%')) / 100 for rate in self.default_commission.split(',')]
        except ValueError:
            return []


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
