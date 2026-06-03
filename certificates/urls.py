from django.urls import path

from . import views

urlpatterns = [
    path("verification/<uuid:certificate_number>/", views.verify_certificate, name="verify_certificate"),
]
