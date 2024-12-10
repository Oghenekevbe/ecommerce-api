from django.contrib import admin
from .models import Seller

# Register your models here.

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "address", "phone_number")


