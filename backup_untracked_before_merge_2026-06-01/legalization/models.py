from django.conf import settings
from django.db import models


class LegalizationRecord(models.Model):
    document = models.OneToOneField("documents.DocumentRequest", on_delete=models.CASCADE, related_name="legalization")
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    electronic_signature = models.CharField(max_length=255, blank=True)
    legalized_file = models.FileField(upload_to="legalization/files/", blank=True)
    legalized_at = models.DateTimeField(null=True, blank=True)
    public_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Legalisation {self.document.unique_number}"

# Create your models here.
