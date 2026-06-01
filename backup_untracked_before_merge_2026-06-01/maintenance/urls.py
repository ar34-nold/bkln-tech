from django.urls import path

from . import views

urlpatterns = [
    path("", views.maintenance_home, name="maintenance_home"),
    path("demande/", views.request_maintenance, name="request_maintenance"),
]
