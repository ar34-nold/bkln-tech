from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "two_factor_enabled", "updated_at")
    list_filter = ("role", "two_factor_enabled")
    search_fields = ("user__username", "user__email", "phone", "organization")

# Register your models here.
