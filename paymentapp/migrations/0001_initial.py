# Generated by Django 4.2.7 on 2024-04-07 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("store", "0021_delete_paymentmodel"),
    ]

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
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.cart"
                    ),
                ),
            ],
        ),
    ]
