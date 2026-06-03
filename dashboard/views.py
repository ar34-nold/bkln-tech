from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from blog.models import Article
from courses.models import Course
from documents.models import DocumentRequest
from maintenance.models import MaintenanceRequest
from orders.models import Order
from payments.models import Payment
from products.models import Product
from support.models import Ticket
from academy.models import Enrollment


def is_admin_user(user):
    if not (user.is_active and user.is_superuser):
        return False
    allowed_usernames = getattr(settings, "ADMIN_ALLOWED_USERNAMES", [])
    allowed_emails = getattr(settings, "ADMIN_ALLOWED_EMAILS", [])
    if allowed_usernames and user.username not in allowed_usernames:
        return False
    if allowed_emails and user.email not in allowed_emails:
        return False
    return True


@user_passes_test(is_admin_user, login_url="login")
def dashboard(request):
    stats = {
        "produits": Product.objects.count(),
        "commandes": Order.objects.count(),
        "formations": Course.objects.count(),
        "documents": DocumentRequest.objects.count(),
        "maintenance": MaintenanceRequest.objects.count(),
        "paiements": Payment.objects.count(),
        "tickets": Ticket.objects.count(),
        "articles": Article.objects.count(),
    }
    recent_enrollments = Enrollment.objects.filter(paid=False).select_related("student", "course").order_by("-enrolled_at")[:6]
    modules = [
        {"title": "Utilisateurs", "description": "Comptes, roles, profils et acces.", "url": "/admin/auth/user/", "image": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=900&q=80"},
        {"title": "Produits boutique", "description": "Catalogue, prix, stock et images.", "url": "/admin/products/product/", "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80"},
        {"title": "Commandes", "description": "Commandes clients et references Mobile Money.", "url": "/admin/orders/order/", "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=900&q=80"},
        {"title": "Formations", "description": "Cours, chapitres, lecons et quiz.", "url": "/admin/courses/course/", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=900&q=80"},
        {"title": "Documents", "description": "Demandes, legalisation et verification publique.", "url": "/admin/documents/documentrequest/", "image": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80"},
        {"title": "Maintenance", "description": "Demandes, techniciens et rapports.", "url": "/admin/maintenance/maintenancerequest/", "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=80"},
        {"title": "Support", "description": "Tickets, reponses et suivi client.", "url": "/admin/support/ticket/", "image": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80"},
        {"title": "Blog", "description": "Articles, categories et commentaires.", "url": "/admin/blog/article/", "image": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=900&q=80"},
    ]
    shortcuts = [
        {"label": "Administration Django", "url": "/admin/"},
        {"label": "Ajouter un produit", "url": "/admin/products/product/add/"},
        {"label": "Ajouter une formation", "url": "/admin/courses/course/add/"},
        {"label": "Voir les commandes", "url": "/admin/orders/order/"},
        {"label": "Messages contact", "url": "/admin/website/contactmessage/"},
        {"label": "Demandes de devis", "url": "/admin/website/quoterequest/"},
    ]
    return render(request, "dashboard/home.html", {"stats": stats, "modules": modules, "shortcuts": shortcuts, "recent_enrollments": recent_enrollments})

# Create your views here.
