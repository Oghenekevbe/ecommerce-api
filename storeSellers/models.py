from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.




class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store_sellers')
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


