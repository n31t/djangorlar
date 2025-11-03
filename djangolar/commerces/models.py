from enum import Enum
from django.contrib.auth import get_user_model
from django.db import models
from catalogs.models import Dishes, Restaurants, Options


User = get_user_model()

class Addresses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Orders(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = 'new'
        CONFIRMED = 'confirmed'
        DELIVERING = 'delivering'
        DONE = 'done'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Addresses, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=OrderStatus.choices)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItemOptions(models.Model):
    order_item = models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payments(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending'
        AUTHORIZED = 'authorized'
        FAILED = 'failed'
        REFUNDED = 'refunded'

    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    amount = models.IntegerField()
    method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class Promos(models.Model):
    code = models.CharField(max_length=255)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderPromos(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    promo = models.ForeignKey(Promos, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





