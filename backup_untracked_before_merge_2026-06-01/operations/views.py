from io import BytesIO
from urllib.parse import quote

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .forms import (
    AntivirusSubscriptionForm,
    ClientForm,
    CustomerOrderForm,
    MaintenanceForm,
    NetworkInterventionForm,
    OSInstallationForm,
    ProductForm,
    RentalForm,
    SaleForm,
    SaleItemFormSet,
)
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
)


def catalog(request):
    categories = Product.Category.choices
    selected = request.GET.get("categorie", "")
    products = Product.objects.filter(actif=True)
    if selected:
        products = products.filter(categorie=selected)
    return render(
        request,
        "operations/catalog.html",
        {"products": products, "categories": categories, "selected": selected},
    )


def order_product(request, pk):
    product = get_object_or_404(Product, pk=pk, actif=True)
    if request.method == "POST":
        form = CustomerOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.produit = product
            if order.moyen_paiement == CustomerOrder.PaymentMethod.ORANGE_MONEY:
                order.statut_paiement = CustomerOrder.PaymentStatus.PENDING
            order.save()
            payment = order.get_moyen_paiement_display()
            message = (
                "Bonjour BKLN-TECH SOLUTIONS, je veux commander ce produit.%0A"
                f"Produit: {product.nom}%0A"
                f"Quantite: {order.quantite}%0A"
                f"Total: {order.total} FCFA%0A"
                f"Nom: {order.nom_client}%0A"
                f"Telephone: {order.telephone}%0A"
                f"Adresse: {order.adresse or 'Non renseignee'}%0A"
                f"Paiement: {payment}%0A"
            )
            if order.moyen_paiement == CustomerOrder.PaymentMethod.ORANGE_MONEY:
                message += (
                    f"Numero Orange Money: {order.numero_orange_money}%0A"
                    f"Reference Orange Money: {order.reference_orange_money}%0A"
                )
            if order.message:
                message += f"Message: {order.message}%0A"
            return redirect(f"https://wa.me/22172343776?text={quote(message, safe='%')}")
    else:
        form = CustomerOrderForm()
    return render(request, "operations/order_form.html", {"form": form, "product": product})


@login_required
def dashboard(request):
    totals = {
        "clients": Client.objects.count(),
        "produits": Product.objects.count(),
        "ventes": Sale.objects.count(),
        "locations": Rental.objects.count(),
        "maintenances": Maintenance.objects.exclude(statut=Maintenance.Status.DELIVERED).count(),
        "commandes": CustomerOrder.objects.filter(statut=CustomerOrder.Status.NEW).count(),
        "stock_faible": Product.objects.filter(stock__lte=3, actif=True).count(),
    }
    ventes_recentes = Sale.objects.select_related("client").prefetch_related("lignes")[:5]
    maintenances = Maintenance.objects.select_related("client")[:5]
    revenus = Sale.objects.aggregate(total=Sum("lignes__prix_unitaire"))["total"] or 0
    modules = [
        ("Ventes", "sale_list", "Enregistrer les ventes et imprimer les factures."),
        ("Commandes", "order_list", "Voir les commandes envoyees par les clients."),
        ("Locations", "rental_list", "Suivre les ordinateurs loues et les retours."),
        ("Maintenance", "maintenance_list", "Gerer reparations, fiches techniques et recus."),
        ("Systemes", "os_list", "Planifier les installations Windows et Linux."),
        ("Antivirus", "antivirus_list", "Suivre licences, abonnements et renouvellements."),
        ("Reseaux", "network_list", "Gerer installations et maintenances reseau."),
        ("Catalogue", "catalog", "Voir la vitrine client et les produits commandables."),
    ]
    return render(
        request,
        "operations/dashboard.html",
        {
            "totals": totals,
            "ventes_recentes": ventes_recentes,
            "maintenances": maintenances,
            "revenus": revenus,
            "modules": modules,
        },
    )


class BaseListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q and hasattr(self, "search_fields"):
            query = None
            from django.db.models import Q

            for field in self.search_fields:
                current = Q(**{f"{field}__icontains": q})
                query = current if query is None else query | current
            queryset = queryset.filter(query)
        return queryset


class ClientListView(BaseListView):
    model = Client
    template_name = "operations/object_list.html"
    context_object_name = "objects"
    search_fields = ["nom", "telephone", "email"]
    extra_context = {"title": "Clients", "create_url": "client_create", "columns": ["nom", "telephone", "email"]}


class CustomerOrderListView(BaseListView):
    model = CustomerOrder
    template_name = "operations/order_list.html"
    context_object_name = "orders"
    search_fields = ["nom_client", "telephone", "produit__nom", "reference_orange_money"]

    def get_queryset(self):
        return super().get_queryset().select_related("produit")


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "operations/form.html"
    success_url = reverse_lazy("client_list")
    extra_context = {"title": "Nouveau client"}


class ProductListView(BaseListView):
    model = Product
    template_name = "operations/object_list.html"
    context_object_name = "objects"
    search_fields = ["nom", "categorie"]
    extra_context = {"title": "Produits", "create_url": "product_create", "columns": ["nom", "categorie", "prix", "stock"]}


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "operations/form.html"
    success_url = reverse_lazy("product_list")
    extra_context = {"title": "Nouveau produit"}


class SaleListView(BaseListView):
    model = Sale
    template_name = "operations/sale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        return Sale.objects.select_related("client").prefetch_related("lignes__produit")


@login_required
def sale_create(request):
    sale = Sale()
    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale)
        if form.is_valid() and formset.is_valid():
            sale = form.save()
            formset.instance = sale
            formset.save()
            messages.success(request, "Vente enregistree avec succes.")
            return redirect("sale_list")
    else:
        form = SaleForm(instance=sale)
        formset = SaleItemFormSet(instance=sale)
    return render(request, "operations/sale_form.html", {"form": form, "formset": formset, "title": "Nouvelle vente"})


@login_required
def sale_invoice_pdf(request, pk):
    sale = get_object_or_404(Sale.objects.select_related("client").prefetch_related("lignes__produit"), pk=pk)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 60
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "BKLN-TECH SOLUTIONS")
    y -= 25
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, "Facture de vente de materiels et services informatiques")
    y -= 35
    pdf.drawString(50, y, f"Facture N: {sale.pk}")
    pdf.drawString(350, y, f"Date: {sale.date:%d/%m/%Y}")
    y -= 20
    pdf.drawString(50, y, f"Client: {sale.client.nom}")
    y -= 35
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Produit")
    pdf.drawString(300, y, "Qte")
    pdf.drawString(360, y, "PU")
    pdf.drawString(450, y, "Total")
    y -= 15
    pdf.setFont("Helvetica", 10)
    for item in sale.lignes.all():
        pdf.drawString(50, y, item.produit.nom[:38])
        pdf.drawString(300, y, str(item.quantite))
        pdf.drawString(360, y, f"{item.prix_unitaire:.2f}")
        pdf.drawString(450, y, f"{item.total:.2f}")
        y -= 18
    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(360, y, "Total")
    pdf.drawString(450, y, f"{sale.total:.2f}")
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"facture-{sale.pk}.pdf")


class RentalListView(BaseListView):
    model = Rental
    template_name = "operations/rental_list.html"
    context_object_name = "rentals"

    def get_queryset(self):
        return Rental.objects.select_related("client", "materiel")


class RentalCreateView(LoginRequiredMixin, CreateView):
    model = Rental
    form_class = RentalForm
    template_name = "operations/form.html"
    success_url = reverse_lazy("rental_list")
    extra_context = {"title": "Nouvelle location"}


class MaintenanceListView(BaseListView):
    model = Maintenance
    template_name = "operations/maintenance_list.html"
    context_object_name = "maintenances"

    def get_queryset(self):
        return Maintenance.objects.select_related("client")


class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = "operations/form.html"
    success_url = reverse_lazy("maintenance_list")
    extra_context = {"title": "Nouvelle maintenance"}


class OSInstallationListView(BaseListView):
    model = OSInstallation
    template_name = "operations/object_list.html"
    context_object_name = "objects"
    extra_context = {"title": "Installations OS", "create_url": "os_create", "columns": ["client", "appareil", "systeme", "prix"]}


class OSInstallationCreateView(LoginRequiredMixin, CreateView):
    model = OSInstallation
    form_class = OSInstallationForm
    template_name = "operations/form.html"
    success_url = reverse_lazy("os_list")
    extra_context = {"title": "Nouvelle installation OS"}


class AntivirusListView(BaseListView):
    model = AntivirusSubscription
    template_name = "operations/object_list.html"
    context_object_name = "objects"
    extra_context = {"title": "Antivirus", "create_url": "antivirus_create", "columns": ["client", "marque", "date_expiration", "actif"]}


class AntivirusCreateView(LoginRequiredMixin, CreateView):
    model = AntivirusSubscription
    form_class = AntivirusSubscriptionForm
    template_name = "operations/form.html"
    success_url = reverse_lazy("antivirus_list")
    extra_context = {"title": "Nouvel antivirus"}


class NetworkListView(BaseListView):
    model = NetworkIntervention
    template_name = "operations/object_list.html"
    context_object_name = "objects"
    extra_context = {"title": "Reseaux", "create_url": "network_create", "columns": ["client", "type_intervention", "date_intervention", "terminee"]}


class NetworkCreateView(LoginRequiredMixin, CreateView):
    model = NetworkIntervention
    form_class = NetworkInterventionForm
    template_name = "operations/form.html"
    success_url = reverse_lazy("network_list")
    extra_context = {"title": "Nouvelle intervention reseau"}
