from django.urls import path

from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("nouveau/", views.ticket_create, name="ticket_create"),
]
