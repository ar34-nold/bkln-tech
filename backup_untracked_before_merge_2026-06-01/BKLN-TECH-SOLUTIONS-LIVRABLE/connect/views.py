from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView

from .forms import CitizenRegistrationForm, CriminalRecordRequestForm, DocumentRequestForm
from .models import CriminalRecordRequest, DocumentRequest, UserProfile


class HomeView(TemplateView):
    template_name = "connect/home.html"


class RegisterView(CreateView):
    template_name = "connect/register.html"
    form_class = CitizenRegistrationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Votre compte a été créé avec succès. Veuillez vous connecter.")
        return super().form_valid(form)


@login_required
def dashboard(request):
    profile = getattr(request.user, "profile", None)
    document_requests = DocumentRequest.objects.filter(citizen=request.user)[:6]
    casier_requests = CriminalRecordRequest.objects.filter(citizen=request.user)[:6]
    return render(request, "connect/dashboard.html", {
        "profile": profile,
        "document_requests": document_requests,
        "casier_requests": casier_requests,
    })


@login_required
def submit_document_request(request):
    form = DocumentRequestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        document_request = form.save(commit=False)
        document_request.citizen = request.user
        document_request.statut = DocumentRequest.Status.SUBMITTED
        document_request.save()
        messages.success(request, "Votre demande de légalisation a été enregistrée.")
        return redirect(document_request.get_absolute_url())
    return render(request, "connect/document_request_form.html", {"form": form})


@login_required
def submit_casier_request(request):
    form = CriminalRecordRequestForm(request.POST or None)
    if form.is_valid():
        casier_request = form.save(commit=False)
        casier_request.citizen = request.user
        casier_request.paiement = CriminalRecordRequest.PaymentStatus.UNPAID
        casier_request.save()
        messages.success(request, "Votre demande de casier judiciaire a été soumise.")
        return redirect("connect:dashboard")
    return render(request, "connect/casier_request_form.html", {"form": form})


class DocumentDetailView(DetailView):
    model = DocumentRequest
    template_name = "connect/document_detail.html"
    context_object_name = "document_request"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.profile.role != UserProfile.Role.CITIZEN:
            return DocumentRequest.objects.all()
        return DocumentRequest.objects.filter(citizen=self.request.user)


def public_verify(request):
    code = request.GET.get("code")
    document_request = None
    matched = False
    if code:
        try:
            document_request = DocumentRequest.objects.get(verification_code=code)
            matched = True
        except DocumentRequest.DoesNotExist:
            matched = False
    return render(request, "connect/public_verify.html", {"document_request": document_request, "matched": matched})
