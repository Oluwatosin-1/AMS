from django.db import models
from django.conf import settings 
from django.db.models import Sum
from django.db.models.functions import TruncMonth 
from django.db.models import Count, Sum
from products.models import ProductPurchase
from referrals.models import Referral 
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
        
    def get_rank_title(self):
        if hasattr(self, 'rank') and self.rank.current_rank:
            return self.rank.current_rank.title
        return "No Rank"

    def get_performance_data(self):
        """Generate performance data for the affiliate."""
        performance_data = ProductPurchase.objects.filter(affiliate=self).annotate(
            month=TruncMonth('purchased_at')
        ).values('month').annotate(
            total_sales=Count('id'),
            total_commissions=Sum('commission_earned')
        ).order_by('month')

        chart_labels = [data['month'].strftime('%b %Y') for data in performance_data]
        chart_sales = [data['total_sales'] for data in performance_data]
        chart_commissions = [data['total_commissions'] for data in performance_data]

        return {
            'chart_labels': chart_labels,
            'chart_sales': chart_sales,
            'chart_commissions': chart_commissions,
        }

    def calculate_total_earnings(self):
        """Calculate total earnings including product commissions, referrals, and rank rewards."""
        product_commissions = self.productpurchase_set.aggregate(
            total=Sum('commission_earned')
        )['total'] or 0

        referral_commissions = Referral.objects.filter(affiliate=self).aggregate(
            total=Sum('commission_earned')
        )['total'] or 0

        rank_rewards = self.rank.current_rank.reward if hasattr(self, 'rank') and self.rank.current_rank else 0

        return product_commissions + referral_commissions + rank_rewards


    def __str__(self):
        return self.user.username 

class AffiliateEarning(models.Model):
    EARNING_TYPES = [
        ('product', 'Product Commission'),
        ('referral', 'Referral Commission'),
        ('rank', 'Rank Reward'),
    ]
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE, related_name='earnings')
    earning_type = models.CharField(max_length=20, choices=EARNING_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.affiliate.user.username} - {self.earning_type} - ${self.amount}"
