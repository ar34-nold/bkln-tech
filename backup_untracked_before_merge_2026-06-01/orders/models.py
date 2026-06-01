from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.product.current_price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Nouvelle"
        PAID = "paid", "Payee"
        PROCESSING = "processing", "En preparation"
        DELIVERED = "delivered", "Livree"
        CANCELLED = "cancelled", "Annulee"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    reference = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    payment_method = models.CharField(max_length=60, default="mobile_money")
    payment_target = models.CharField(max_length=40, default="72 34 37 76")
    payment_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def total(self):
        return self.unit_price * self.quantity

# Create your models here.
