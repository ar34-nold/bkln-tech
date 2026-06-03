from django.urls import path

from . import views

urlpatterns = [
    path("inscription/", views.register, name="register"),
    path("profil/", views.profile, name="profile"),
]
