from django.urls import path

from . import views


urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("catalogue/", views.catalog, name="catalog_legacy"),
    path("catalogue/commander/<int:pk>/", views.order_product, name="order_product"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/nouveau/", views.ClientCreateView.as_view(), name="client_create"),
    path("produits/", views.ProductListView.as_view(), name="product_list"),
    path("produits/nouveau/", views.ProductCreateView.as_view(), name="product_create"),
    path("ventes/", views.SaleListView.as_view(), name="sale_list"),
    path("ventes/nouvelle/", views.sale_create, name="sale_create"),
    path("ventes/<int:pk>/facture/", views.sale_invoice_pdf, name="sale_invoice_pdf"),
    path("locations/", views.RentalListView.as_view(), name="rental_list"),
    path("locations/nouvelle/", views.RentalCreateView.as_view(), name="rental_create"),
    path("maintenances/", views.MaintenanceListView.as_view(), name="maintenance_list"),
    path("maintenances/nouvelle/", views.MaintenanceCreateView.as_view(), name="maintenance_create"),
    path("installations-os/", views.OSInstallationListView.as_view(), name="os_list"),
    path("installations-os/nouvelle/", views.OSInstallationCreateView.as_view(), name="os_create"),
    path("antivirus/", views.AntivirusListView.as_view(), name="antivirus_list"),
    path("antivirus/nouveau/", views.AntivirusCreateView.as_view(), name="antivirus_create"),
    path("reseaux/", views.NetworkListView.as_view(), name="network_list"),
    path("reseaux/nouvelle/", views.NetworkCreateView.as_view(), name="network_create"),
]
