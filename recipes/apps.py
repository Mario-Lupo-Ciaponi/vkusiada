from django.apps import AppConfig


class VkusiadaAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"

    def ready(self):
        from recipes import signals
