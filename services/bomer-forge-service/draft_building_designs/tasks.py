from celery import shared_task, Task
import structlog

logger = structlog.get_logger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def generate_bill_of_materials_for_building_component_task(
    self: Task,
    *,
    draft_building_design_building_component_uuid: str,
):
    from draft_building_designs.services.ai_drawing_component_footing_bom_calculation import (
        generate_bill_of_materials_for_component as generate_bill_of_materials_for_component_service,
    )
    from draft_building_designs.models import DraftBuildingDesignBuildingComponent

    draft_building_design_building_component = (
        DraftBuildingDesignBuildingComponent.objects.get(
            uuid=draft_building_design_building_component_uuid
        )
    )

    type_str = str(draft_building_design_building_component.building_component.type)

    logger.info(
        "Generating bill of materials for building component",
        type_str=type_str,
    )
    generate_bill_of_materials_for_component_service(
        draft_building_design_building_component_uuid=draft_building_design_building_component_uuid,
    )
