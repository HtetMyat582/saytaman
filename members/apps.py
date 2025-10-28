from django.apps import AppConfig


class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'members'

    def ready(self):
        # import signals to register them
        try:
            import members.signals  # noqa: F401
        except Exception:
            pass
