from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("a-propos/", views.static_page, {"template_name": "website/about.html", "title": "A propos"}, name="about"),
    path("services/", views.static_page, {"template_name": "website/services.html", "title": "Nos services"}, name="services"),
    path("formations/", views.static_page, {"template_name": "website/trainings.html", "title": "Nos formations"}, name="trainings"),
    path("realisations/", views.static_page, {"template_name": "website/portfolio.html", "title": "Nos realisations"}, name="portfolio"),
    path("faq/", views.static_page, {"template_name": "website/faq.html", "title": "FAQ"}, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("devis/", views.quote_request, name="quote_request"),
]
