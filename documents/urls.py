from django.urls import path

from . import views

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("nouveau/", views.submit_document, name="submit_document"),
    path("verification/<uuid:unique_number>/", views.public_verify, name="document_verify"),
]
