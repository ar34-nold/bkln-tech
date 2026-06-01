from django import forms
from django.contrib.auth.models import User

from .models import Profile


class SimpleRegistrationForm(forms.Form):
    full_name = forms.CharField(
        label="Nom complet",
        max_length=160,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre nom complet"}),
    )
    phone = forms.CharField(
        label="Telephone",
        max_length=40,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: 70 03 92 69"}),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Votre mot de passe"}),
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        username = "".join(char for char in phone if char.isdigit())
        if not username:
            raise forms.ValidationError("Veuillez indiquer un numero de telephone valide.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Un compte existe deja avec ce numero.")
        return phone

    def save(self):
        full_name = self.cleaned_data["full_name"].strip()
        phone = self.cleaned_data["phone"].strip()
        username = "".join(char for char in phone if char.isdigit())
        parts = full_name.split(" ", 1)
        user = User.objects.create_user(
            username=username,
            password=self.cleaned_data["password"],
            first_name=parts[0],
            last_name=parts[1] if len(parts) > 1 else "",
        )
        Profile.objects.create(user=user, phone=phone)
        return user
