from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    DesignDrawingComponentMetadata,
    DesignDrawingComponentMetadataSubtype,
)
from .tasks import ai_calculate_design_drawing_component_bom
import structlog

logger = structlog.get_logger(__name__)


@receiver(post_save, sender=DesignDrawingComponentMetadata)
def post_save_design_drawing_component_metadata(sender, instance, created, **kwargs):
    """
    Calculate the bill of materials for a design drawing component.
    """
    if created and instance.subtype == DesignDrawingComponentMetadataSubtype.FOOTING:
        logger.info(
            "Calculating bill of materials for design drawing component",
            design_drawing_component_metadata_uuid=str(instance.uuid),
        )
        task_id = ai_calculate_design_drawing_component_bom.delay(
            design_drawing_component_metadata_uuid=str(instance.uuid)
        )
        instance.task_id = task_id
        instance.save()
