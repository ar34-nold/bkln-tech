from django.contrib import admin

from .models import (
    AntivirusSubscription,
    Client,
    CustomerOrder,
    Maintenance,
    NetworkIntervention,
    OSInstallation,
    Product,
    Rental,
    Sale,
    SaleItem,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "email", "cree_le")
    search_fields = ("nom", "telephone", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nom", "categorie", "prix", "stock", "actif")
    list_filter = ("categorie", "actif")
    search_fields = ("nom",)


@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = (
        "nom_client",
        "telephone",
        "produit",
        "quantite",
        "total",
        "moyen_paiement",
        "statut_paiement",
        "statut",
        "cree_le",
    )
    list_filter = ("moyen_paiement", "statut_paiement", "statut", "cree_le")
    search_fields = ("nom_client", "telephone", "produit__nom", "reference_orange_money")


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "date", "payee")
    list_filter = ("payee", "date")
    inlines = [SaleItemInline]


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("client", "materiel", "date_debut", "date_fin", "cout_total", "statut")
    list_filter = ("statut",)


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("client", "appareil", "service", "statut", "cout", "cree_le")
    list_filter = ("service", "statut")
    search_fields = ("client__nom", "appareil", "numero_serie")


@admin.register(OSInstallation)
class OSInstallationAdmin(admin.ModelAdmin):
    list_display = ("client", "appareil", "systeme", "licence_fournie", "prix", "cree_le")
    list_filter = ("systeme", "licence_fournie")


@admin.register(AntivirusSubscription)
class AntivirusSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("client", "marque", "date_activation", "date_expiration", "actif")
    list_filter = ("marque", "actif")


@admin.register(NetworkIntervention)
class NetworkInterventionAdmin(admin.ModelAdmin):
    list_display = ("client", "type_intervention", "date_intervention", "cout", "terminee")
    list_filter = ("type_intervention", "terminee")
