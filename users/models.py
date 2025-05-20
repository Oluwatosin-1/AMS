from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    USER_TYPES = (
        ("admin", "Admin"),
        ("affiliate", "Affiliate"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="affiliate")

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """Profile model to store additional user information."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    tax_identification_number = models.CharField(max_length=50, null=True, blank=True)
    preferred_payment_method = models.CharField(
        max_length=20,
        choices=[("paypal", "PayPal"), ("bank_transfer", "Bank Transfer")],
        default="paypal",
    )
    bank_account_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
