from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import redirect, render

from .models import Ticket


@login_required
def ticket_list(request):
    return render(request, "generic/list.html", {"title": "Support client", "objects": Ticket.objects.filter(user=request.user), "fields": ["subject", "status", "created_at"]})


@login_required
def ticket_create(request):
    Form = modelform_factory(Ticket, fields=("subject", "message"))
    form = Form(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect("ticket_list")
    return render(request, "generic/form.html", {"title": "Nouveau ticket", "form": form})

# Create your views here.
