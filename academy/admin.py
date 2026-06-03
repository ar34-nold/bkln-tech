from django.contrib import admin

from .models import Enrollment
from academy import signals as academy_signals
from django.conf import settings


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
	list_display = ("id", "student", "course", "paid", "enrolled_at")
	list_filter = ("paid", "enrolled_at")
	search_fields = ("student__username", "student__email", "course__title")
	actions = ["mark_as_paid"]

	def _format_phone(self, phone):
		if not phone:
			return None
		digits = "".join(ch for ch in phone if ch.isdigit())
		if not digits:
			return None
		# If number looks local (<=8 digits), assume Cameroon +236
		if len(digits) <= 8:
			return "+236" + digits
		if digits.startswith("236"):
			return "+" + digits
		if digits.startswith("0"):
			return "+236" + digits.lstrip("0")
		return "+" + digits

	@admin.action(description="Marquer les inscriptions sélectionnées comme payées")
	def mark_as_paid(self, request, queryset):
		count = 0
		for enrollment in queryset.select_related("student"):
			if not enrollment.paid:
				enrollment.paid = True
				enrollment.save()
				# send confirmation WhatsApp to student if phone available
				phone = None
				profile = getattr(enrollment.student, "profile", None)
				if profile:
					phone = profile.phone
				# fallback to user attribute 'phone' if exists
				if not phone:
					phone = getattr(enrollment.student, "phone", None)
				formatted = self._format_phone(phone)
				if formatted:
					# determine language preference: profile.language -> user.language -> settings.LANGUAGE_CODE -> 'fr'
					profile_lang = None
					profile = getattr(enrollment.student, "profile", None)
					if profile:
						profile_lang = getattr(profile, "language", None)
					user_lang = getattr(enrollment.student, "language", None)
					lang = profile_lang or user_lang or getattr(settings, "LANGUAGE_CODE", "fr")
					try:
						body = academy_signals.build_student_payment_confirmation(enrollment, lang=lang)
						academy_signals.send_whatsapp_message(body, formatted)
					except Exception:
						# don't block admin action on failure
						pass
				count += 1
		self.message_user(request, f"{count} inscription(s) marquée(s) comme payée(s).")

# Register your models here.
