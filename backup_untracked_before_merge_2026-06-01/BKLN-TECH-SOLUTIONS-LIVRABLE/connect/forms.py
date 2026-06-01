from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CriminalRecordRequest, DocumentRequest, UserProfile


class CitizenRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Adresse email valide")
    telephone = forms.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "telephone", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=UserProfile.Role.CITIZEN,
                telephone=self.cleaned_data["telephone"],
            )
        return user


class DocumentRequestForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = ["titre", "description", "fichier"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Type de document"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "fichier": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class CriminalRecordRequestForm(forms.ModelForm):
    class Meta:
        model = CriminalRecordRequest
        fields = ["date_naissance", "lieu_naissance", "motif"]
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "lieu_naissance": forms.TextInput(attrs={"class": "form-control"}),
            "motif": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
