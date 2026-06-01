from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render

from .models import DocumentRequest


@login_required
def submit_document(request):
    Form = modelform_factory(DocumentRequest, fields=("document_type", "title", "file"))
    form = Form(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        doc = form.save(commit=False)
        doc.user = request.user
        doc.save()
        return redirect("document_list")
    return render(request, "generic/form.html", {"title": "Televerser un document", "form": form})


@login_required
def document_list(request):
    return render(request, "generic/list.html", {"title": "Documents", "objects": DocumentRequest.objects.filter(user=request.user), "fields": ["title", "document_type", "status", "unique_number"]})


def public_verify(request, unique_number):
    document = get_object_or_404(DocumentRequest, unique_number=unique_number)
    return render(request, "documents/verify.html", {"document": document})

# Create your views here.
