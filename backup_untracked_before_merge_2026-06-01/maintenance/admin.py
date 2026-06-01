from django.contrib import admin

from .models import InterventionReport, MaintenanceRequest

admin.site.register(MaintenanceRequest)
admin.site.register(InterventionReport)

# Register your models here.
