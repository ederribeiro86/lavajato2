from django.apps import AppConfig
from django.db.models.signals import post_migrate


def seed_default_services(sender, **kwargs):
    from .models import Servico
    Servico.ensure_default_servicos()


class LavajatoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lavajato'

    def ready(self):
        post_migrate.connect(seed_default_services, sender=self.__class__)
