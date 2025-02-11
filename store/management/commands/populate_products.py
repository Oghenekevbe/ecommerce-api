import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Product, Category, Seller
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with 500 fake products'

    def handle(self, *args, **kwargs):
        user = User.objects.get(id=1)  # Using user 1 as requested
        categories = list(Category.objects.all())
        sellers = list(Seller.objects.all())

        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Add some categories first.'))
            return
        
        if not sellers:
            self.stdout.write(self.style.ERROR('No sellers found. Add some sellers first.'))
            return
        
        products = []
        for _ in range(10000):
            category = random.choice(categories)
            seller = random.choice(sellers)
            discount_percentage = Decimal(random.uniform(0, 50)).quantize(Decimal('0.00'))

            product = Product(
                created_by=user,
                updated_by=user,
                name=fake.unique.company(),
                description=fake.text(),
                category=category,
                price=Decimal(random.uniform(10, 500)).quantize(Decimal('0.00')),
                is_available=random.choice([True, False]),
                discount_percentage=discount_percentage,
                currency='NGN',
                sku=fake.unique.bothify(text='???-######'),
                manufacturer=fake.company(),
                stock_quantity=random.randint(0, 500),
                restock_threshold=random.randint(5, 20),
                promo=None,  # Leave promo blank
                seller=seller,
            )
            products.append(product)

        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS('Successfully added 10000 fake products!'))
