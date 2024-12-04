from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from decimal import Decimal 


class Product(models.Model):
    """Product model with commission rates."""
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
        help_text="Comma-separated percentages, e.g., 5%, 2%",
        validators=[RegexValidator(r'^(\d+%,?)+$', 'Enter valid comma-separated percentages.')]
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='others')
    status = models.BooleanField(default=True, verbose_name="Active Status")
    sales_note = models.TextField(null=True, blank=True, help_text="Noted when sales occur")
    keywords = models.TextField(help_text="Keywords to describe the product for search optimization")
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_commission_rates(self):
        """
        Parse and return the commission rates as a list of floats.
        """
        try:
            return [float(rate.strip('%')) / 100 for rate in self.default_commission.split(',')]
        except ValueError:
            return []

    def get_commission_rate(self):
        """
        Return the first commission rate or default to 0.05 (5%).
        """
        rates = self.get_commission_rates()
        return rates[0] if rates else 0.05

    def __str__(self):
        return self.name


class AffiliateProductLink(models.Model):
    """
    Model for linking affiliates to products with unique tracking URLs.
    """
    affiliate = models.ForeignKey('affiliates.Affiliate', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    unique_url = models.URLField(unique=True)
    clicks = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """
        Override save to dynamically generate a unique URL if not provided.
        """
        if not self.unique_url:
            self.unique_url = (
                f"{reverse('product_detail', kwargs={'pk': self.product.id})}?ref={self.affiliate.user.id}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.affiliate.user.username} - {self.product.name}"


class ProductPurchase(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    affiliate = models.ForeignKey('affiliates.Affiliate', on_delete=models.SET_NULL, null=True, blank=True)
    client_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paystack_reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.affiliate:
            commission_rate = self.product.get_commission_rate()
            self.commission_earned = Decimal(self.amount) * Decimal(commission_rate)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.client_email} - {self.is_paid}"