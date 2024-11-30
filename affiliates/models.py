from django.db import models 
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.conf import settings  # Use settings for AUTH_USER_MODEL
from django.db import models 

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('affiliate', 'Affiliate'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='affiliate')

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username 


class Affiliate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Correct reference
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    training_completed = models.BooleanField(default=False)
    referrals = models.PositiveIntegerField(default=0)
    payout_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=50.0)

    def __str__(self):
        return self.user.username
