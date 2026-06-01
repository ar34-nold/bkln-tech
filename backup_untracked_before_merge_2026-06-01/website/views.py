from django.contrib import messages
from django.shortcuts import redirect, render

from blog.models import Article
from courses.models import Course
from products.models import Product

from .models import Banner, ContactMessage, NewsletterSubscriber, QuoteRequest, Service, Testimonial


FEATURES = [
    {
        "title": "Boutique informatique",
        "description": "Ordinateurs, accessoires, logiciels, antivirus et paiement Orange Money.",
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
        "url_name": "product_list",
    },
    {
        "title": "Maintenance informatique",
        "description": "Diagnostic, reparation, installation Windows/Linux et depannage reseau.",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=80",
        "url_name": "request_maintenance",
    },
    {
        "title": "Logiciels et antivirus",
        "description": "Installation, configuration et protection avec Kaspersky et outils professionnels.",
        "image": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=900&q=80",
        "url_name": "product_list",
    },
    {
        "title": "BKLN-TECH Academy",
        "description": "Formations en bureautique, developpement web, Django, API REST et IA.",
        "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80",
        "url_name": "course_list",
    },
    {
        "title": "Documents administratifs",
        "description": "Televersement, verification, legalisation, QR Code et suivi en ligne.",
        "image": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80",
        "url_name": "submit_document",
    },
    {
        "title": "Support client",
        "description": "Tickets, suivi des demandes et assistance rapide par equipe technique.",
        "image": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80",
        "url_name": "ticket_create",
    },
]


def home(request):
    if request.method == "POST" and request.POST.get("newsletter_email"):
        NewsletterSubscriber.objects.get_or_create(email=request.POST["newsletter_email"])
        messages.success(request, "Inscription a la newsletter enregistree.")
        return redirect("home")
    return render(request, "website/home.html", {
        "banners": Banner.objects.filter(active=True)[:3],
        "services": Service.objects.filter(active=True)[:8],
        "testimonials": Testimonial.objects.filter(active=True)[:6],
        "products": Product.objects.filter(active=True, featured=True)[:6],
        "courses": Course.objects.filter(published=True)[:6],
        "articles": Article.objects.filter(published=True)[:3],
        "features": FEATURES,
    })


def static_page(request, template_name, title):
    return render(request, template_name, {"page_title": title, "services": Service.objects.filter(active=True), "features": FEATURES})


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
            subject=request.POST.get("subject", "Contact BKLN-TECH"),
            message=request.POST.get("message", ""),
        )
        messages.success(request, "Votre message a ete envoye.")
        return redirect("contact")
    return render(request, "website/contact.html")


def quote_request(request):
    if request.method == "POST":
        QuoteRequest.objects.create(
            name=request.POST.get("name", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
            service=request.POST.get("service", ""),
            budget=request.POST.get("budget") or None,
            details=request.POST.get("details", ""),
        )
        messages.success(request, "Votre demande de devis a ete transmise.")
        return redirect("quote_request")
    return render(request, "website/quote.html", {"services": Service.objects.filter(active=True)})

# Create your views here.
