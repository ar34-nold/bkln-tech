from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "connect"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("inscription/", views.RegisterView.as_view(), name="register"),
    path("connexion/", auth_views.LoginView.as_view(template_name="connect/login.html"), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(next_page="connect:home"), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("documents/nouvelle/", views.submit_document_request, name="submit_document_request"),
    path("documents/<int:pk>/", views.DocumentDetailView.as_view(), name="document_detail"),
    path("casier/nouveau/", views.submit_casier_request, name="submit_casier_request"),
    path("verifier/", views.public_verify, name="public_verify"),
    path("api/", include("connect.api_urls")),
]
