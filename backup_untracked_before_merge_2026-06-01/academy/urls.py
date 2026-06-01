from django.urls import path

from . import views

urlpatterns = [
    path("", views.student_space, name="academy_home"),
]
