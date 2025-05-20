from django.db import models
from affiliates.models import Affiliate


class Rank(models.Model):
    """Rank model to manage affiliate ranks."""

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="rank_logos/", null=True, blank=True)
    node_color = models.CharField(max_length=7, default="#000000")  # Hex color code

    # Rank rules
    min_personal_referrals = models.PositiveIntegerField(default=0)
    min_total_referrals = models.PositiveIntegerField(default=0)

    # Rank rewards
    reward = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    personal_referral_commission = models.DecimalField(
        max_digits=5, decimal_places=2, default=5.0
    )  # %
    initial_level_commission = models.DecimalField(
        max_digits=5, decimal_places=2, default=5.0
    )  # %
    renewal_level_commission = models.DecimalField(
        max_digits=5, decimal_places=2, default=5.0
    )  # %

    admin_note = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)  # Rank visibility

    def __str__(self):
        return self.title


class AffiliateRank(models.Model):
    """Link affiliates to ranks."""

    affiliate = models.OneToOneField(
        Affiliate, on_delete=models.CASCADE, related_name="rank"
    )
    current_rank = models.ForeignKey(
        Rank, on_delete=models.SET_NULL, null=True, blank=True
    )
    achieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.affiliate.user.username} - {self.current_rank.title if self.current_rank else 'No Rank'}"
