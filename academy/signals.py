import logging
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Enrollment

logger = logging.getLogger(__name__)


def send_whatsapp_message(body, to):
    try:
        from twilio.rest import Client
    except Exception:
        logger.warning("Twilio not installed; skipping WhatsApp notification.")
        return
    sid = getattr(settings, "TWILIO_ACCOUNT_SID", None)
    token = getattr(settings, "TWILIO_AUTH_TOKEN", None)
    from_number = getattr(settings, "TWILIO_WHATSAPP_FROM", None)
    if not (sid and token and from_number and to):
        logger.info("Twilio settings incomplete; skipping WhatsApp notification.")
        return
    try:
        client = Client(sid, token)
        client.messages.create(body=body, from_=f"whatsapp:{from_number}", to=f"whatsapp:{to}")
        logger.info("WhatsApp notification sent to %s", to)
    except Exception as e:
        logger.exception("Failed to send WhatsApp message: %s", e)


def build_student_payment_confirmation(enrollment, lang="fr"):
    name = enrollment.student.get_full_name() or enrollment.student.username
    course = enrollment.course.title
    if lang and lang.lower().startswith("en"):
        return (
            f"Hello {name},\nYour enrollment for the course '{course}' has been confirmed as paid.\nThank you for choosing us."
        )
    # default to French
    return (
        f"Bonjour {name},\nVotre inscription à la formation '{course}' a été confirmée comme payée.\nMerci d'avoir choisi BKLN-TECH."
    )


@receiver(post_save, sender=Enrollment)
def enrollment_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    # Only notify for unpaid enrollments
    if instance.paid:
        return
    admin_whatsapp = getattr(settings, "ADMIN_WHATSAPP_NUMBER", None)
    if not admin_whatsapp:
        # fallback to existing constant used in templates
        admin_whatsapp = "+23670039269"

    student_name = getattr(instance.student, "get_full_name", None)
    if callable(student_name):
        student_name = instance.student.get_full_name() or instance.student.username
    else:
        student_name = getattr(instance.student, "username", "Utilisateur")

    body = (
        f"Nouvelle demande d'inscription\n"
        f"Étudiant: {student_name}\n"
        f"Formation: {instance.course.title}\n"
        f"ID inscription: {instance.id}\n"
        f"Date: {instance.enrolled_at.strftime('%Y-%m-%d %H:%M')}"
    )

    send_whatsapp_message(body, admin_whatsapp)
