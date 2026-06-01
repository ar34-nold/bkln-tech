from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import redirect, render

from .models import CriminalRecordRequest


@login_required
def criminal_record_list(request):
    return render(request, "generic/list.html", {"title": "Casier judiciaire", "objects": CriminalRecordRequest.objects.filter(user=request.user), "fields": ["request_number", "status", "created_at"]})


@login_required
def criminal_record_create(request):
    Form = modelform_factory(CriminalRecordRequest, fields=("birth_place", "birth_date", "identity_document"))
    form = Form(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return redirect("criminal_record_list")
    return render(request, "generic/form.html", {"title": "Demande de casier judiciaire", "form": form})

# Create your views here.
