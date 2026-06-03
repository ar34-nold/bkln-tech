from django.urls import path

from . import views

urlpatterns = [
    path("", views.criminal_record_list, name="criminal_record_list"),
    path("demande/", views.criminal_record_create, name="criminal_record_create"),
]
