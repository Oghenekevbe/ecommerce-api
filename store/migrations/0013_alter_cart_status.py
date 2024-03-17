# Generated by Django 4.2.7 on 2024-02-04 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0012_delete_sellerorders"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[
                    ("unconfirmed", "Unconfirmed"),
                    ("confirmed", "Confirmed"),
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                    ("returned", "Returned"),
                ],
                default="Unconfirmed",
                max_length=20,
                null=True,
            ),
        ),
    ]