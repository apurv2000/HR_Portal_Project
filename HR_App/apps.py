

from django.apps import AppConfig

class HRAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HR_App'

    def ready(self):
        from . import scheduler
        scheduler.start()

