from django.db import models
from affiliates.models import Affiliate

# Centralized Status Choices
STATUS_CHOICES = [
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("processed", "Processed"),
    ("failed", "Failed"),
]


# Abstract Base Model
class BasePayout(models.Model):
    """Abstract base class for payout and payment-related models."""

    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.CASCADE,
        related_name="%(class)s_payouts",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.affiliate.user.username} - {self.amount} ({self.status})"


# Derived Models
class PayoutRequest(BasePayout):
    """Model for affiliate payout requests."""

    pass


class Payout(BasePayout):
    """Model for processed payouts."""

    affiliate = models.ForeignKey(
        Affiliate,
        on_delete=models.CASCADE,
        related_name="payouts",  # Explicitly set the related name
    )
    processed_at = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Payout of ${self.amount} to {self.affiliate.user.username} - {self.status}"


class Payment(BasePayout):
    """Model for tracking general affiliate payments."""

    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment to {self.affiliate.user.username}: {self.amount}"
