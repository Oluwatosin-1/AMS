# Generated by Django 5.1.2 on 2024-12-02 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingmodule",
            name="material",
            field=models.FileField(
                blank=True, null=True, upload_to="training_materials/"
            ),
        ),
        migrations.AddField(
            model_name="trainingprogress",
            name="admin_verified",
            field=models.BooleanField(default=False),
        ),
    ]
