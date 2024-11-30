from django.db import models
from django.conf import settings  # Use settings for AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    USER_TYPES = (
        ('admin', 'Admin'),
        ('affiliate', 'Affiliate'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='affiliate')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Affiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    training_completed = models.BooleanField(default=False)
    referrals = models.PositiveIntegerField(default=0)
    payout_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50.0)

    # Genealogy for referral tracking
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals_downline'
    )

    def __str__(self):
        return self.user.username
