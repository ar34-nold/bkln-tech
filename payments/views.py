from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Payment


@login_required
def payment_list(request):
    return render(request, "generic/list.html", {"title": "Paiements", "objects": Payment.objects.filter(user=request.user), "fields": ["reference", "amount", "status", "method"]})

# Create your views here.
