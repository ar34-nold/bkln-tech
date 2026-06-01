from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.quiz_detail, name="quiz_detail"),
]
