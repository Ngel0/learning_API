from django.apps import AppConfig


class CryptodataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cryptodata'

    def ready(self):
        from . import scheduler
        scheduler.schedule_cryptocurrency_data_update()
