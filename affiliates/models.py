from django.db import models
from django.conf import settings
from .managers import AffiliateManager  # Custom manager for Affiliates

class BaseModel(models.Model):
    """Abstract base class for models with timestamp fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Affiliate(BaseModel):
    """Model for managing affiliate information."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    training_completed = models.BooleanField(default=False)
    referrals = models.PositiveIntegerField(default=0)
    payout_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50.0)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals_downline'
    )

    objects = AffiliateManager()  # Attach custom manager

    def increase_referrals(self):
        self.referrals += 1
        self.save()

    def __str__(self):
        return self.user.username
