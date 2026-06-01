from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import (
    CustomTokenObtainPairView,
    CriminalRecordRequestViewSet,
    DocumentRequestViewSet,
    MeAPIView,
    RegisterAPIView,
)

router = DefaultRouter()
router.register(r"documents", DocumentRequestViewSet, basename="documents")
router.register(r"casier", CriminalRecordRequestViewSet, basename="casier")

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="api_register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", MeAPIView.as_view(), name="api_me"),
    path("", include(router.urls)),
]
