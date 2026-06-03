import uuid

from django.conf import settings
from django.db import models


class CriminalRecordRequest(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Soumise"
        REVIEW = "review", "En verification"
        APPROVED = "approved", "Approuvee"
        DELIVERED = "delivered", "Delivree"
        REJECTED = "rejected", "Rejetee"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    request_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    birth_place = models.CharField(max_length=160)
    birth_date = models.DateField()
    identity_document = models.FileField(upload_to="criminal_records/ids/")
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUBMITTED)
    secure_pdf = models.FileField(upload_to="criminal_records/pdf/", blank=True)
    qr_code = models.ImageField(upload_to="criminal_records/qr/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.request_number)

# Create your models here.
