from django.apps import apps

def update_affiliate_rank(affiliate):
    """Update the rank of an affiliate based on referral statistics."""
    Affiliate = apps.get_model('affiliates', 'Affiliate')
    Rank = apps.get_model('ranking', 'Rank')
    AffiliateRank = apps.get_model('ranking', 'AffiliateRank')
    TrainingProgress = apps.get_model('training', 'TrainingProgress')

    total_referrals = Affiliate.objects.filter(referred_by=affiliate).count()
    personal_referrals = affiliate.referrals

    # Training completion check
    completed_trainings = TrainingProgress.objects.filter(user=affiliate.user, completed=True).count()

    # Find the highest eligible rank
    eligible_ranks = Rank.objects.filter(
        min_personal_referrals__lte=personal_referrals,
        min_total_referrals__lte=total_referrals,
        is_active=True
    ).order_by('-min_personal_referrals', '-min_total_referrals')  # Higher ranks first

    for rank in eligible_ranks:
        if completed_trainings >= 3:  # Check if training threshold is met
            affiliate_rank, created = AffiliateRank.objects.get_or_create(affiliate=affiliate)
            if affiliate_rank.current_rank != rank:
                affiliate_rank.current_rank = rank
                affiliate_rank.achieved_at = now()
                affiliate_rank.save()
                print(f"Affiliate {affiliate.user.username} promoted to rank: {rank.title}")
                return rank
    return None
