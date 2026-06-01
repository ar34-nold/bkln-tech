from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CriminalRecordRequest, DocumentRequest
from .serializers import (
    CriminalRecordRequestSerializer,
    DocumentRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class DocumentRequestViewSet(viewsets.ModelViewSet):
    queryset = DocumentRequest.objects.all()
    serializer_class = DocumentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(citizen=self.request.user)

    def get_queryset(self):
        if self.request.user.profile.role == self.request.user.profile.Role.CITIZEN:
            return self.queryset.filter(citizen=self.request.user)
        return self.queryset


class CriminalRecordRequestViewSet(viewsets.ModelViewSet):
    queryset = CriminalRecordRequest.objects.all()
    serializer_class = CriminalRecordRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(citizen=self.request.user)

    def get_queryset(self):
        if self.request.user.profile.role == self.request.user.profile.Role.CITIZEN:
            return self.queryset.filter(citizen=self.request.user)
        return self.queryset


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
