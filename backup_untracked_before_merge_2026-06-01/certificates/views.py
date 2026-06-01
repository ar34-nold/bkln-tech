from django.shortcuts import get_object_or_404, render

from .models import Certificate


def verify_certificate(request, certificate_number):
    return render(request, "certificates/verify.html", {"certificate": get_object_or_404(Certificate, certificate_number=certificate_number)})

# Create your views here.
