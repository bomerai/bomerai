from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DraftBuildingDesignBuildingComponent
from .tasks import generate_bill_of_materials_for_building_component_task
import structlog

logger = structlog.get_logger(__name__)


@receiver(post_save, sender=DraftBuildingDesignBuildingComponent)
def post_save_draft_building_design_building_component(
    sender, instance: DraftBuildingDesignBuildingComponent, created, **kwargs
):
    """
    Calculate the bill of materials for a design drawing component.
    """
    if created:
        logger.info(
            "Generating bill of materials for building component",
            draft_building_design_building_component_uuid=str(instance.uuid),
        )
        task_id = generate_bill_of_materials_for_building_component_task.delay(
            draft_building_design_building_component_uuid=str(instance.uuid)
        )
        instance.task_id = task_id
        instance.save(update_fields=["task_id"])
