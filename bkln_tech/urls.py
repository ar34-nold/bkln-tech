from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from api_views import api_articles, api_courses, api_home, api_products


def superuser_admin_permission(request):
    if not (request.user.is_active and request.user.is_superuser):
        return False
    allowed_usernames = getattr(settings, "ADMIN_ALLOWED_USERNAMES", [])
    allowed_emails = getattr(settings, "ADMIN_ALLOWED_EMAILS", [])
    if allowed_usernames and request.user.username not in allowed_usernames:
        return False
    if allowed_emails and request.user.email not in allowed_emails:
        return False
    return True


admin.site.has_permission = superuser_admin_permission
admin.site.site_header = "Administration BKLN-TECH"
admin.site.site_title = "BKLN-TECH Admin"
admin.site.index_title = "Gestion complete du site"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_home, name="api_home"),
    path("api/products/", api_products, name="api_products"),
    path("api/courses/", api_courses, name="api_courses"),
    path("api/articles/", api_articles, name="api_articles"),
    path("connexion/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("comptes/", include("accounts.urls")),
    path("boutique/", include("products.urls")),
    path("commandes/", include("orders.urls")),
    path("stock/", include("inventory.urls")),
    path("maintenance/", include("maintenance.urls")),
    path("locations/", include("rentals.urls")),
    path("documents/", include("documents.urls")),
    path("legalisation/", include("legalization.urls")),
    path("casier-judiciaire/", include("criminal_records.urls")),
    path("academy/", include("academy.urls")),
    path("cours/", include("courses.urls")),
    path("lecons/", include("lessons.urls")),
    path("quiz/", include("quizzes.urls")),
    path("certificats/", include("certificates.urls")),
    path("paiements/", include("payments.urls")),
    path("blog/", include("blog.urls")),
    path("support/", include("support.urls")),
    path("admin-dashboard/", include("dashboard.urls")),
    path("notifications/", include("notifications.urls")),
    path("operations/", include("operations.urls", namespace="operations")),
    path("", include("website.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
