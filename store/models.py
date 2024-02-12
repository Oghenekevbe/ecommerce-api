from datetime import datetime
from decimal import Decimal
from django.core.validators import MaxValueValidator
from django.db import models
from user.models import User
import uuid

# Create your models here.

class Product(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields
    sku = models.CharField(max_length=50, unique=True)
    manufacturer = models.CharField(max_length=255, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    restock_threshold = models.PositiveIntegerField(default=10)

    #promotion on product

    promo = models.ForeignKey('Promotion', on_delete=models.CASCADE, null = True, blank=True)

    # User association (e.g., creator or owner)
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, null=True)




    @property
    def discounted_price(self):
        """
        Calculate the discounted price based on the discount percentage.
        """
        if self.discount_percentage == 0 and not self.promo:
            return None
    
        elif self.discount_percentage is not None and not self.promo:
            discount_factor = 1 - (self.discount_percentage / 100)
            discounted_price = Decimal(self.price) * Decimal(discount_factor)
            discounted_price = discounted_price.quantize(Decimal('0.00'))
            return discounted_price
        
        elif self.promo is not None and self.discount_percentage == 0:
            promotion_discount_factor = 1 - (self.promo.discount_percentage / 100)
            discounted_price = Decimal(promotion_discount_factor) * Decimal(self.price)
        
            discounted_price = discounted_price.quantize(Decimal('0.00'))
            return discounted_price
        else:
            return "you either put in a discount percentage or promo or nothing at all. you can't put in both"



        
        

    
    @property
    def stock_status(self):
        """
        Determine the stock status based on the restock threshold.
        """
        if self.stock_quantity <= 0:
            return "Out of Stock"
        elif self.stock_quantity <= self.restock_threshold:
            return "Low Stock - Time to Order"
        else:
            return "Above Restock Threshold - Still Good"

    def __str__(self):
        return self.name
    


class Promotion(models.Model):
    promo_name = models.CharField(max_length=50)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    start_date = models.DateTimeField(help_text='Please use the format YYYY-MM-DD')
    end_date = models.DateTimeField(help_text='Please use the format YYYY-MM-DD')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.promo_name
    
    def save(self, *args, **kwargs):
        today = datetime.now().date()
        start_date = self.start_date.date()
        end_date = self.end_date.date()

        print("Today:", today)
        print("Start Date:", start_date)
        print("End Date:", end_date)

        if start_date <= today <= end_date:
            # Promotion is currently active
            self.discount_percentage = self.discount_percentage
        else:
            # Promotion has ended or not yet started
            self.discount_percentage = 0

        print("Discount Percentage:", self.discount_percentage)

        super().save(*args, **kwargs)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])  # You can adjust this based on your rating scale
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.product}  rating:  {self.rating}/5'

    
    


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.company_name
    



class BillingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='billing_addresses')
    address = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_billing_address = models.BooleanField(default=False)

    
    def __str__(self):
        
        if self.address is not None:
            return f'{self.address}, {self.city}'
        else:
            return "No Billing Address"
        


ORDER_STATUS_CHOICES = (
    ('unconfirmed', 'Unconfirmed'),
    ('confirmed', 'Confirmed'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('returned', 'Returned'),
)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(BillingAddress, related_name='billing_address', on_delete=models.CASCADE,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, null=True, default = 'Unconfirmed')    
    order_number = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)    
    
    def __str__(self):
        return str(self.user.username) + ' - ' + str(self.order_number)
    
    @property
    def cart_total(self):
        cart_items = self.cart_items.all()
        total = sum([item.get_total for item in cart_items])
        return total

    @property
    def cart_item_count(self):
        return self.cart_items.count()


ORDER_ITEM_STATUS_CHOICES = (
    ('unconfirmed', 'Unconfirmed'),
    ('confirmed', 'Confirmed'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('returned', 'Returned'),
)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Cart, related_name='cart_items' , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_ITEM_STATUS_CHOICES, null=True, default = 'Unconfirmed')    


    def __str__(self):
        if self.product:
            return self.product.name
        else:
            return 'Order Item ' + str(self.id)
        
    @property
    def get_total(self):

        price_to_use = self.product.discounted_price if self.product.discounted_price is not None else self.product.price
        total = self.quantity * price_to_use

        
        return total







class Return(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    returned_item = models.CharField(max_length=50)  # Assuming some identifier for the returned item
    return_reason = models.TextField()
    return_date = models.DateField()




