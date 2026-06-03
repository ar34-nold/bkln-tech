from django.conf import settings
from django.db import models


class MaintenanceRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Nouvelle"
        ASSIGNED = "assigned", "Attribuee"
        IN_PROGRESS = "in_progress", "En intervention"
        DONE = "done", "Terminee"
        CLOSED = "closed", "Cloturee"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="maintenance_requests")
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_maintenance")
    service_type = models.CharField(max_length=120)
    device = models.CharField(max_length=180)
    serial_number = models.CharField(max_length=120, blank=True)
    issue = models.TextField()
    diagnosis = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device} - {self.client}"


class InterventionReport(models.Model):
    request = models.OneToOneField(MaintenanceRequest, on_delete=models.CASCADE, related_name="report")
    work_done = models.TextField()
    recommendations = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to="maintenance/reports/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
