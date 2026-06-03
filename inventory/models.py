from django.db import models


class StockMovement(models.Model):
    class Type(models.TextChoices):
        IN = "in", "Entree"
        OUT = "out", "Sortie"
        ADJUSTMENT = "adjustment", "Ajustement"

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="stock_movements")
    movement_type = models.CharField(max_length=20, choices=Type.choices)
    quantity = models.IntegerField()
    reason = models.CharField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.quantity}"


class Promotion(models.Model):
    name = models.CharField(max_length=160)
    products = models.ManyToManyField("products.Product", related_name="promotions", blank=True)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Create your models here.
