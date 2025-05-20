from django.db import models


class AffiliateManager(models.Manager):
    def active_affiliates(self):
        """Fetch all active affiliates."""
        return self.filter(user__is_active=True)

    def top_referrers(self):
        """Fetch affiliates with the most referrals."""
        return self.order_by("-referrals")[:10]
