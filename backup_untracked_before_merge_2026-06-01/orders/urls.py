from django.urls import path

from . import views

urlpatterns = [
    path("", views.order_list, name="order_list_new"),
    path("commander/<int:product_id>/", views.quick_order, name="quick_order"),
]
