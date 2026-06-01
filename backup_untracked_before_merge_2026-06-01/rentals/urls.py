from django.urls import path

from . import views

urlpatterns = [
    path("", views.rental_catalog, name="rental_catalog"),
    path("reserver/", views.reserve_item, name="reserve_item"),
]
