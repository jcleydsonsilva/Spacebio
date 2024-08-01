from django.apps import AppConfig
import os

class SpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'space'

    def ready(self):
        pass
