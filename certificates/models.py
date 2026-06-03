import uuid

from django.conf import settings
from django.db import models


class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="certificates")
    course = models.ForeignKey("courses.Course", on_delete=models.PROTECT)
    certificate_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    pdf_file = models.FileField(upload_to="certificates/pdf/", blank=True)
    qr_code = models.ImageField(upload_to="certificates/qr/", blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.certificate_number)

# Create your models here.
