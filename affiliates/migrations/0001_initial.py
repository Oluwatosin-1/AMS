# Generated by Django 5.1.2 on 2024-12-01 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Affiliate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "commission_rate",
                    models.DecimalField(decimal_places=2, default=5.0, max_digits=5),
                ),
                ("training_completed", models.BooleanField(default=False)),
                ("referrals", models.PositiveIntegerField(default=0)),
                (
                    "payout_threshold",
                    models.DecimalField(decimal_places=2, default=50.0, max_digits=10),
                ),
                (
                    "referred_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="referrals_downline",
                        to="affiliates.affiliate",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
