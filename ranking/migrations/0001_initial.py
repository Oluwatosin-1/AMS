# Generated by Django 5.1.2 on 2024-12-02 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("affiliates", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rank",
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
                ("title", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "logo",
                    models.ImageField(blank=True, null=True, upload_to="rank_logos/"),
                ),
                ("node_color", models.CharField(default="#000000", max_length=7)),
                ("min_personal_referrals", models.PositiveIntegerField(default=0)),
                ("min_total_referrals", models.PositiveIntegerField(default=0)),
                (
                    "reward",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "personal_referral_commission",
                    models.DecimalField(decimal_places=2, default=5.0, max_digits=5),
                ),
                (
                    "initial_level_commission",
                    models.DecimalField(decimal_places=2, default=5.0, max_digits=5),
                ),
                (
                    "renewal_level_commission",
                    models.DecimalField(decimal_places=2, default=5.0, max_digits=5),
                ),
                ("admin_note", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="AffiliateRank",
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
                ("achieved_at", models.DateTimeField(auto_now_add=True)),
                (
                    "affiliate",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rank",
                        to="affiliates.affiliate",
                    ),
                ),
                (
                    "current_rank",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="ranking.rank",
                    ),
                ),
            ],
        ),
    ]
