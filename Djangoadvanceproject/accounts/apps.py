from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Djangoadvanceproject.accounts'

    def ready(self):
        import Djangoadvanceproject.accounts.signals