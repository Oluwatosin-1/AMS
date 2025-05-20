from django.db.models.signals import post_save
from django.dispatch import receiver
from ranking.utils import update_affiliate_rank
from referrals.models import Referral
from users.models import CustomUser, UserProfile


@receiver(post_save, sender=Referral)
def handle_new_referral(sender, instance, created, **kwargs):
    """Signal to update the rank of the affiliate after a new referral."""
    if created:
        referrer = instance.affiliate
        referrer.increase_referrals()
        update_affiliate_rank(referrer)


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
