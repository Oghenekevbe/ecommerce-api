# Generated by Django 4.2.7 on 2023-12-13 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="seller",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="store.product",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="store.category"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="seller",
            field=models.ManyToManyField(blank=True, to="store.seller"),
        ),
        migrations.AddField(
            model_name="product",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_items",
                to="store.cart",
            ),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="store.product"
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="address",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="billing_address",
                to="store.billingaddress",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="billingaddress",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="billing_addresses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
