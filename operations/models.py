from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(TimeStampedModel):
    nom = models.CharField(max_length=160)
    telephone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    adresse = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Product(TimeStampedModel):
    class Category(models.TextChoices):
        LAPTOP = "laptop", "Ordinateur portable"
        DESKTOP = "desktop", "Ordinateur de bureau"
        PRINTER = "printer", "Imprimante"
        ACCESSORY = "accessory", "Accessoire"
        STORAGE = "storage", "Disque dur"
        ANTIVIRUS = "antivirus", "Antivirus"

    nom = models.CharField(max_length=180)
    categorie = models.CharField(max_length=30, choices=Category.choices)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True)
    image_externe = models.URLField(blank=True)
    prix = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["categorie", "nom"]

    def __str__(self):
        return self.nom


class CustomerOrder(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "Nouvelle"
        CONFIRMED = "confirmed", "Confirmee"
        DELIVERED = "delivered", "Livree"
        CANCELLED = "cancelled", "Annulee"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Paiement a la livraison"
        ORANGE_MONEY = "orange_money", "Orange Money"

    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", "Non paye"
        PENDING = "pending", "En attente de verification"
        PAID = "paid", "Paye"
        FAILED = "failed", "Echec"

    produit = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="commandes")
    nom_client = models.CharField(max_length=160)
    telephone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    quantite = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    moyen_paiement = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    numero_orange_money = models.CharField(max_length=40, blank=True)
    reference_orange_money = models.CharField(max_length=80, blank=True)
    statut_paiement = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    message = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return f"Commande {self.produit} - {self.nom_client}"

    @property
    def total(self):
        return self.produit.prix * self.quantite


class Sale(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="ventes")
    date = models.DateField(default=timezone.localdate)
    remise = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    payee = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"Vente #{self.pk} - {self.client}"

    @property
    def total(self):
        total_lignes = sum((ligne.total for ligne in self.lignes.all()), Decimal("0"))
        return max(total_lignes - self.remise, Decimal("0"))


class SaleItem(models.Model):
    vente = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="lignes")
    produit = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.produit} x {self.quantite}"

    @property
    def total(self):
        return self.prix_unitaire * self.quantite


class Rental(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "En cours"
        RETURNED = "returned", "Retourne"
        LATE = "late", "En retard"

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="locations")
    materiel = models.ForeignKey(Product, on_delete=models.PROTECT)
    date_debut = models.DateField(default=timezone.localdate)
    date_fin = models.DateField()
    cout_journalier = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    statut = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    date_retour = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-date_debut"]

    def __str__(self):
        return f"Location {self.materiel} - {self.client}"

    @property
    def duree_jours(self):
        return max((self.date_fin - self.date_debut).days + 1, 1)

    @property
    def cout_total(self):
        return self.cout_journalier * self.duree_jours


class Maintenance(TimeStampedModel):
    class Status(models.TextChoices):
        RECEIVED = "received", "Recu"
        IN_PROGRESS = "in_progress", "En reparation"
        DONE = "done", "Termine"
        DELIVERED = "delivered", "Livre"

    class ServiceType(models.TextChoices):
        FORMAT = "formatage", "Formatage"
        WINDOWS = "windows", "Reinstallation Windows"
        HARDWARE = "hardware", "Reparation materielle"
        CLEANING = "cleaning", "Nettoyage logiciel"
        UPDATE = "update", "Mise a jour systeme"

    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="maintenances")
    appareil = models.CharField(max_length=180)
    numero_serie = models.CharField(max_length=120, blank=True)
    service = models.CharField(max_length=40, choices=ServiceType.choices)
    panne_declaree = models.TextField()
    diagnostic = models.TextField(blank=True)
    cout = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    statut = models.CharField(max_length=30, choices=Status.choices, default=Status.RECEIVED)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.appareil} - {self.client}"


class OSInstallation(TimeStampedModel):
    class System(models.TextChoices):
        WINDOWS_11 = "windows_11", "Windows 11"
        WINDOWS_10 = "windows_10", "Windows 10"
        UBUNTU = "ubuntu", "Ubuntu"
        LINUX_MINT = "linux_mint", "Linux Mint"

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    appareil = models.CharField(max_length=180)
    systeme = models.CharField(max_length=30, choices=System.choices)
    licence_fournie = models.BooleanField(default=False)
    prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.get_systeme_display()} - {self.client}"


class AntivirusSubscription(TimeStampedModel):
    class Brand(models.TextChoices):
        KASPERSKY = "kaspersky", "Kaspersky"
        AVAST = "avast", "Avast"
        ESET = "eset", "ESET NOD32"
        BITDEFENDER = "bitdefender", "Bitdefender"

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    marque = models.CharField(max_length=30, choices=Brand.choices)
    cle_licence = models.CharField(max_length=120, blank=True)
    date_activation = models.DateField(default=timezone.localdate)
    date_expiration = models.DateField()
    prix = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["date_expiration"]

    def __str__(self):
        return f"{self.get_marque_display()} - {self.client}"


class NetworkIntervention(TimeStampedModel):
    class Type(models.TextChoices):
        INSTALL = "installation", "Installation reseau"
        ROUTER = "routeur", "Configuration routeur"
        SHARING = "partage", "Partage de connexion"
        MONITORING = "surveillance", "Surveillance reseau"
        MAINTENANCE = "maintenance", "Maintenance reseau"

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    type_intervention = models.CharField(max_length=40, choices=Type.choices)
    technologies = models.CharField(max_length=255, help_text="Ex: RJ45, Wi-Fi, Switch, Routeur")
    description = models.TextField()
    date_intervention = models.DateField(default=timezone.localdate)
    cout = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    terminee = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_intervention"]

    def __str__(self):
        return f"{self.get_type_intervention_display()} - {self.client}"
