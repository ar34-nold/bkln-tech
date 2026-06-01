import uuid

from django.conf import settings
from django.db import models


class DocumentRequest(models.Model):
    class Type(models.TextChoices):
        DIPLOMA = "diploma", "Diplome"
        ATTESTATION = "attestation", "Attestation"
        CERTIFICATE = "certificate", "Certificat"
        TRANSCRIPT = "transcript", "Releve de notes"
        ADMIN = "admin", "Document administratif"

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Soumis"
        REVIEW = "review", "Verification"
        APPROVED = "approved", "Valide"
        REJECTED = "rejected", "Rejete"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    document_type = models.CharField(max_length=30, choices=Type.choices)
    title = models.CharField(max_length=180)
    file = models.FileField(upload_to="documents/uploads/")
    unique_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUBMITTED)
    qr_code = models.ImageField(upload_to="documents/qr/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Create your models here.
