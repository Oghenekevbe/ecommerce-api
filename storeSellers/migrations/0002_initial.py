# Generated by Django 4.2.7 on 2024-08-12 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("storeSellers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="seller",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="store_sellers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]