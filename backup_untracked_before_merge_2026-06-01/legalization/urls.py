from django.urls import path

from . import views

urlpatterns = [
    path("verification/", views.legalization_verify, name="legalization_verify"),
]
