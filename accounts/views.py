from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import redirect, render

from .forms import SimpleRegistrationForm
from .models import Profile


def register(request):
    form = SimpleRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Compte cree avec succes.")
        return redirect("home")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    ProfileForm = modelform_factory(Profile, fields=("role", "phone", "address", "organization", "avatar", "two_factor_enabled", "language"))
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profil mis a jour.")
        return redirect("profile")
    return render(request, "accounts/profile.html", {"form": form})

# Create your views here.
