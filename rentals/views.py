from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import redirect, render

from .models import RentalItem, Reservation


def rental_catalog(request):
    return render(request, "rentals/catalog.html", {"items": RentalItem.objects.filter(available=True)})


@login_required
def reserve_item(request):
    Form = modelform_factory(Reservation, fields=("item", "starts_on", "ends_on"))
    form = Form(request.POST or None)
    if request.method == "POST" and form.is_valid():
        reservation = form.save(commit=False)
        reservation.client = request.user
        reservation.save()
        return redirect("rental_catalog")
    return render(request, "generic/form.html", {"title": "Reservation de materiel", "form": form})

# Create your views here.
