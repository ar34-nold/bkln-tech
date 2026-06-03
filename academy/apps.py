from django.apps import AppConfig


class AcademyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academy'
    def ready(self):
        try:
            import academy.signals  # noqa: F401
        except Exception:
            pass
