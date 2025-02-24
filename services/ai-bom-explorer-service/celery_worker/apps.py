from django.apps import AppConfig


class CeleryWorkerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_worker'
