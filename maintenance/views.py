from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import redirect, render

from .models import MaintenanceRequest


@login_required
def request_maintenance(request):
    Form = modelform_factory(MaintenanceRequest, fields=("service_type", "device", "serial_number", "issue"))
    form = Form(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.client = request.user
        item.save()
        messages.success(request, "Demande de maintenance enregistree.")
        return redirect("maintenance_home")
    return render(request, "generic/form.html", {"title": "Demande de maintenance", "form": form})


@login_required
def maintenance_home(request):
    return render(request, "generic/list.html", {"title": "Maintenance", "objects": MaintenanceRequest.objects.filter(client=request.user), "fields": ["device", "service_type", "status"]})

# Create your views here.
