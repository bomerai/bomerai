from django.apps import AppConfig


class DraftBuildingDesignsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "draft_building_designs"

    def ready(self):
        from . import signals
