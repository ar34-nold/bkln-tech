from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CriminalRecordRequest, DocumentRequest, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["role", "telephone", "organisation"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    telephone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password", "telephone"]

    def create(self, validated_data):
        telephone = validated_data.pop("telephone")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, telephone=telephone, role=UserProfile.Role.CITIZEN)
        return user


class DocumentRequestSerializer(serializers.ModelSerializer):
    citizen = UserSerializer(read_only=True)

    class Meta:
        model = DocumentRequest
        fields = [
            "id",
            "request_number",
            "citizen",
            "titre",
            "description",
            "fichier",
            "statut",
            "verification_code",
            "qr_code",
            "document_pdf",
            "cree_le",
            "modifie_le",
        ]
        read_only_fields = ["request_number", "citizen", "statut", "verification_code", "qr_code", "document_pdf"]


class CriminalRecordRequestSerializer(serializers.ModelSerializer):
    citizen = UserSerializer(read_only=True)

    class Meta:
        model = CriminalRecordRequest
        fields = [
            "id",
            "request_number",
            "citizen",
            "date_naissance",
            "lieu_naissance",
            "motif",
            "statut",
            "paiement",
            "document_pdf",
            "cree_le",
            "modifie_le",
        ]
        read_only_fields = ["request_number", "citizen", "statut", "paiement", "document_pdf"]
