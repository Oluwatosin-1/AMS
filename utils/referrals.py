from referrals.models import Referral


def track_referral_commission(product_purchase):
    # Ensure the affiliate and referrer relationships are tracked
    affiliate = product_purchase.affiliate
    if affiliate and affiliate.referred_by:
        referrer = affiliate.referred_by
        commission_rate = referrer.commission_rate  # Percentage commission
        commission = product_purchase.amount * (commission_rate / 100)

        # Update commission earned for the referrer
        Referral.objects.create(
            affiliate=referrer,
            product=product_purchase.product,
            commission_earned=commission,
        )
