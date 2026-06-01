from django.contrib import admin

from .models import ActivityLog, CriminalRecordRequest, DocumentRequest, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "telephone", "organisation", "cree_le"]
    search_fields = ["user__username", "user__email", "telephone"]
    list_filter = ["role"]


@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ["request_number", "titre", "citizen", "statut", "cree_le"]
    list_filter = ["statut"]
    readonly_fields = ["request_number", "verification_code", "qr_code", "document_pdf"]


@admin.register(CriminalRecordRequest)
class CriminalRecordRequestAdmin(admin.ModelAdmin):
    list_display = ["request_number", "citizen", "statut", "paiement", "cree_le"]
    list_filter = ["statut", "paiement"]
    readonly_fields = ["request_number", "document_pdf"]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["action", "user", "cree_le"]
    list_filter = ["user"]
    search_fields = ["action", "details"]
