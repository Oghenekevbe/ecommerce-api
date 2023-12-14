from django.db import models
from user.models import User
import uuid

# Create your models here.

class Product(models.Model):
    '''
        sku: Stock Keeping Unit, a unique identifier for the product.
        manufacturer: The manufacturer or brand of the product.
        stock_quantity: The current quantity of the product in stock.
        restock_threshold: The threshold at which the product should be restocked.
        creator: A ForeignKey linking to the User who created the product. It's nullable, allowing for cases where the creator is not known or has been deleted.
        owners: A ManyToManyField for associating multiple users as owners of the product. This might be useful if you want to track ownership by users.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields
    sku = models.CharField(max_length=50, unique=True)
    manufacturer = models.CharField(max_length=255, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    restock_threshold = models.PositiveIntegerField(default=10)

    # User association (e.g., creator or owner)
    seller = models.ManyToManyField('Seller', blank=True)




    @property
    def discounted_price(self):
        """
        Calculate the discounted price based on the discount percentage.
        """
        discount_factor = 1 - (self.discount_percentage / 100)
        discounted_price = self.price * discount_factor
        return discounted_price
    
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
    


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)  # You can adjust this based on your rating scale
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    


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
    is_no_billing_address = models.BooleanField(default=False)

    
    def __str__(self):
        if self.is_no_billing_address:
            return "No Billing Address"
        elif self.customer is not None and self.customer.user is not None:
            return str(self.customer.user) + ' - ' + self.address
        else:
            return str(self.address)

    class Meta:
        ordering = ('is_no_billing_address', 'id')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(BillingAddress, related_name='billing_address', on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)    
    def __str__(self):
        return str(self.user.username) + ' - ' + str(self.transaction_id)
    
    @property
    def cart_total(self):
        cart_items = self.cart_items.all()
        total = sum([item.get_total() for item in cart_items])
        return total

    @property
    def cart_item_count(self):
        total_items =[item for item in self.cart_items.all()].count()
        return total_items


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Cart, related_name='cart_items' , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return self.product.name
        else:
            return 'Order Item ' + str(self.id)
        
    @property
    def get_total(self):
        total = (self.quantity * self.product.price) - self.product.discounted_price
        return total 

    




