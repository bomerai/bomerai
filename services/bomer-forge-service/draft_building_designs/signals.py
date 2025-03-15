from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DraftBuildingDesignBuildingComponent
import structlog

logger = structlog.get_logger(__name__)


@receiver(post_save, sender=DraftBuildingDesignBuildingComponent)
def post_save_draft_building_design_building_component(
    sender, instance, created, **kwargs
):
    """
    Calculate the bill of materials for a design drawing component.
    """
    pass
