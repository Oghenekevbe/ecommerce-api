# Generated by Django 4.2.7 on 2024-04-07 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0021_delete_paymentmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="currency",
            field=models.CharField(
                choices=[
                    ("USD", "United States Dollar"),
                    ("NGN", "Nigerian Naira"),
                    ("EUR", "Euro"),
                    ("GBP", "British Pound Sterling"),
                    ("GHS", "Ghanaian Cedi"),
                    ("KES", "Kenyan Shilling"),
                    ("ZAR", "South African Rand"),
                    ("UGX", "Ugandan Shilling"),
                    ("CAD", "Canadian Dollar"),
                    ("AUD", "Australian Dollar"),
                    ("JPY", "Japanese Yen"),
                    ("INR", "Indian Rupee"),
                ],
                max_length=3,
                null=True,
            ),
        ),
    ]
