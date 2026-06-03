from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        MANAGER = "manager", "Gestionnaire"
        TRAINER = "trainer", "Formateur"
        CLIENT = "client", "Client"
        STUDENT = "student", "Etudiant"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField("telephone", max_length=40, blank=True)
    address = models.CharField("adresse", max_length=255, blank=True)
    organization = models.CharField("organisation", max_length=160, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    language = models.CharField("langue", max_length=10, choices=[('fr','Français'),('en','English')], default='fr')
    two_factor_enabled = models.BooleanField("2FA activee", default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"

# Create your models here.
