from django import forms
from django.core.exceptions import ValidationError

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


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            if isinstance(field.widget, forms.Select):
                css_class = "form-select"
            field.widget.attrs.update({"class": css_class})


class ClientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nom", "telephone", "email", "adresse"]


class ProductForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ["nom", "categorie", "description", "image", "image_externe", "prix", "stock", "actif"]


class CustomerOrderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = [
            "nom_client",
            "telephone",
            "email",
            "adresse",
            "quantite",
            "moyen_paiement",
            "numero_orange_money",
            "reference_orange_money",
            "message",
        ]
        labels = {
            "numero_orange_money": "Numero Orange Money",
            "reference_orange_money": "Reference de transaction",
        }
        help_texts = {
            "reference_orange_money": "A remplir apres le transfert Orange Money.",
        }

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get("moyen_paiement")
        phone = cleaned_data.get("numero_orange_money")
        reference = cleaned_data.get("reference_orange_money")
        if method == CustomerOrder.PaymentMethod.ORANGE_MONEY and (not phone or not reference):
            raise ValidationError(
                "Pour Orange Money, indiquez le numero utilise et la reference de transaction."
            )
        return cleaned_data


class SaleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["client", "date", "remise", "payee"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class SaleItemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ["produit", "quantite", "prix_unitaire"]


SaleItemFormSet = forms.inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True,
)


class RentalForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Rental
        fields = ["client", "materiel", "date_debut", "date_fin", "cout_journalier", "statut", "date_retour"]
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}),
            "date_fin": forms.DateInput(attrs={"type": "date"}),
            "date_retour": forms.DateInput(attrs={"type": "date"}),
        }


class MaintenanceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ["client", "appareil", "numero_serie", "service", "panne_declaree", "diagnostic", "cout", "statut"]


class OSInstallationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = OSInstallation
        fields = ["client", "appareil", "systeme", "licence_fournie", "prix", "notes"]


class AntivirusSubscriptionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AntivirusSubscription
        fields = ["client", "marque", "cle_licence", "date_activation", "date_expiration", "prix", "actif"]
        widgets = {
            "date_activation": forms.DateInput(attrs={"type": "date"}),
            "date_expiration": forms.DateInput(attrs={"type": "date"}),
        }


class NetworkInterventionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = NetworkIntervention
        fields = ["client", "type_intervention", "technologies", "description", "date_intervention", "cout", "terminee"]
        widgets = {"date_intervention": forms.DateInput(attrs={"type": "date"})}
