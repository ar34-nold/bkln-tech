from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("<slug:slug>/enroll/", views.course_enroll, name="course_enroll"),
    path("<slug:slug>/", views.course_detail, name="course_detail"),
]
