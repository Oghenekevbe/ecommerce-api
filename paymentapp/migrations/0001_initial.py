# Generated by Django 4.2.7 on 2024-05-31 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PaymentModel",
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
                (
                    "mode_of_payment",
                    models.CharField(
                        choices=[
                            ("flutterwave", "Flutterwave"),
                            ("paystack", "Paystack"),
                            ("remita", "Remita"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
            ],
        ),
    ]
