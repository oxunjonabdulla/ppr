from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'apps.core'

    def ready(self):
        from apps.utils import scheduler
        scheduler.start()
