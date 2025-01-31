import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel, AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    username = models.CharField(max_length=150, unique=True) 

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number', 'address']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.name

class Rating(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'Rating {self.rating} for {self.product.name} by {self.user.username}'

class Cart(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_entries'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.user.username}\'s cart'

class Order(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f'Order {self.id} by {self.user.username} - {self.get_status_display()}'

class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.id}'

class Payment(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed')
    ]
    id = models.CharField(primary_key=True, max_length=255)
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    payment_link = models.URLField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f'Payment {self.id} - {self.status}'
