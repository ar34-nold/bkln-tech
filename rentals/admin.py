from django.contrib import admin

from .models import RentalItem, Reservation

admin.site.register(RentalItem)
admin.site.register(Reservation)

# Register your models here.
