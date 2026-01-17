from django.apps import AppConfig


class OnlineStoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_store_app'

    def ready(self):
        import online_store_app.signals
