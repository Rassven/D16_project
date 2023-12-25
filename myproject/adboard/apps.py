from django.apps import AppConfig


class AdboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adboard'

    def ready(self):
        from . import signals
