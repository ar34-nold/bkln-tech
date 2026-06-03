from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.lesson_detail, name="lesson_detail"),
]
