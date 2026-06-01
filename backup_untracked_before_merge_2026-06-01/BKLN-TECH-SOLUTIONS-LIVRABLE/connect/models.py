import io
import uuid
from pathlib import Path

import qrcode
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.signing import Signer
from django.db import models
from django.urls import reverse
from django.utils import timezone
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def upload_document_path(instance, filename):
    return f"documents/{instance.request_number}/{filename}"


def upload_qr_path(instance, filename):
    return f"documents/{instance.request_number}/qr_{filename}"


class TimeStampedModel(models.Model):
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        AGENT_LEGALISATION = "agent_legalisation", "Agent de légalisation"
        AGENT_AUTHENTIFICATION = "agent_authentification", "Agent d'authentification"
        AGENT_CASIER = "agent_casier", "Service de casier judiciaire"
        CITIZEN = "citizen", "Citoyen"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.CITIZEN)
    telephone = models.CharField(max_length=30, blank=True)
    organisation = models.CharField(max_length=180, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_citizen(self):
        return self.role == self.Role.CITIZEN

    @property
    def is_agent(self):
        return self.role in {
            self.Role.AGENT_LEGALISATION,
            self.Role.AGENT_AUTHENTIFICATION,
            self.Role.AGENT_CASIER,
        }


class DocumentRequest(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        SUBMITTED = "submitted", "Soumis"
        VALIDATED = "validated", "Validé"
        REJECTED = "rejected", "Rejeté"
        PROCESSED = "processed", "Traitée"

    request_number = models.CharField(max_length=36, unique=True, editable=False)
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name="document_requests")
    titre = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to=upload_document_path, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    verification_code = models.CharField(max_length=128, blank=True, editable=False)
    qr_code = models.ImageField(upload_to=upload_qr_path, blank=True, null=True)
    document_pdf = models.FileField(upload_to=upload_document_path, blank=True, null=True)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return f"Demande {self.request_number} - {self.titre}"

    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = str(uuid.uuid4())
        if not self.verification_code:
            self.verification_code = Signer().sign(self.request_number)
        super().save(*args, **kwargs)
        if not self.qr_code or not self.document_pdf:
            self.generate_document()

    def get_absolute_url(self):
        return reverse("connect:document_detail", args=[self.pk])

    def generate_document(self):
        qr = qrcode.make(self.verification_code)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        image_content = ContentFile(buf.getvalue(), name=f"qr_{self.request_number}.png")
        self.qr_code.save(image_content.name, image_content, save=False)

        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=LETTER)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Centrafrique Connect", styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"Référence : {self.request_number}", styles["Normal"]),
            Paragraph(f"Demandeur : {self.citizen.get_full_name() or self.citizen.username}", styles["Normal"]),
            Paragraph(f"Titre : {self.titre}", styles["Normal"]),
            Paragraph(f"Statut : {self.get_statut_display()}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph("Code de vérification :", styles["Heading3"]),
            Paragraph(self.verification_code, styles["Code"] if "Code" in styles else styles["Normal"]),
        ]
        doc.build(story)
        pdf_content = ContentFile(pdf_buffer.getvalue(), name=f"document_{self.request_number}.pdf")
        self.document_pdf.save(pdf_content.name, pdf_content, save=False)
        super().save(update_fields=["qr_code", "document_pdf"])


class CriminalRecordRequest(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "Nouvelle"
        REVIEW = "review", "En revue"
        APPROVED = "approved", "Approuvé"
        REJECTED = "rejected", "Rejeté"

    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", "Non payé"
        PENDING = "pending", "En attente"
        PAID = "paid", "Payé"

    request_number = models.CharField(max_length=36, unique=True, editable=False)
    citizen = models.ForeignKey(User, on_delete=models.CASCADE, related_name="casier_requests")
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=180)
    motif = models.CharField(max_length=180, blank=True)
    statut = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    paiement = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    document_pdf = models.FileField(upload_to=upload_document_path, blank=True, null=True)

    class Meta:
        ordering = ["-cree_le"]

    def save(self, *args, **kwargs):
        if not self.request_number:
            self.request_number = str(uuid.uuid4())
        super().save(*args, **kwargs)
        if self.statut == self.Status.APPROVED and not self.document_pdf:
            self.generate_pdf()

    def __str__(self):
        return f"Casier {self.request_number} - {self.citizen}"

    def generate_pdf(self):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=LETTER)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Casier judiciaire en ligne", styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"Référence : {self.request_number}", styles["Normal"]),
            Paragraph(f"Nom : {self.citizen.get_full_name() or self.citizen.username}", styles["Normal"]),
            Paragraph(f"Date de naissance : {self.date_naissance}", styles["Normal"]),
            Paragraph(f"Lieu de naissance : {self.lieu_naissance}", styles["Normal"]),
            Paragraph(f"Statut : {self.get_statut_display()}", styles["Normal"]),
            Spacer(1, 12),
            Paragraph("Ce document est généré automatiquement par Centrafrique Connect.", styles["Italic"]),
        ]
        doc.build(story)
        pdf_content = ContentFile(buffer.getvalue(), name=f"casier_{self.request_number}.pdf")
        self.document_pdf.save(pdf_content.name, pdf_content, save=False)
        super().save(update_fields=["document_pdf"])


class ActivityLog(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.action} ({self.user})"
