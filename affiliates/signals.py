from django.db.models.signals import post_save
from django.dispatch import receiver

from ranking.models import AffiliateRank, Rank
from .models import Affiliate

@receiver(post_save, sender=Affiliate)
def assign_default_rank(sender, instance, created, **kwargs):
    """Assign a default rank to a newly created affiliate."""
    if created and not hasattr(instance, 'rank'):
        default_rank = Rank.objects.filter(is_active=True).order_by('min_personal_referrals').first()
        if default_rank:
            AffiliateRank.objects.create(affiliate=instance, current_rank=default_rank)
