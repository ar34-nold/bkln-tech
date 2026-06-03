from django.conf import settings
from django.db import models


class RentalItem(models.Model):
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    daily_price = models.DecimalField(max_digits=12, decimal_places=2)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        VALIDATED = "validated", "Validee"
        RETURNED = "returned", "Retournee"
        CANCELLED = "cancelled", "Annulee"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    item = models.ForeignKey(RentalItem, on_delete=models.PROTECT)
    starts_on = models.DateField()
    ends_on = models.DateField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    contract_pdf = models.FileField(upload_to="rentals/contracts/", blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} - {self.client}"

# Create your models here.
