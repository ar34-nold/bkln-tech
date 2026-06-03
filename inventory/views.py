from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Promotion, StockMovement


@login_required
def inventory_home(request):
    return render(request, "inventory/home.html", {"movements": StockMovement.objects.select_related("product")[:20], "promotions": Promotion.objects.all()[:10]})

# Create your views here.
