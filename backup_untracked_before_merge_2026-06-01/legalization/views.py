from django.shortcuts import render

from .models import LegalizationRecord


def legalization_verify(request):
    number = request.GET.get("numero")
    record = LegalizationRecord.objects.filter(document__unique_number=number).first() if number else None
    return render(request, "legalization/verify.html", {"record": record, "number": number})

# Create your views here.
