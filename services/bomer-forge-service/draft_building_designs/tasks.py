from celery import shared_task, Task
import structlog

from draft_building_designs.models import (
    DraftBuildingDesign,
    DraftBuildingDesignDrawingDocument,
    DraftBuildingDesignDrawingDocumentType,
    DraftBuildingDesignStatus,
)
from building_components.models import BuildingComponent, BuildingComponentType
from draft_building_designs.services.ai.draft_design_building_components_measure import (
    extract_footings_from_image as extract_footings_from_image_service,
)

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


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def create_draft_building_design_components(
    self: Task, *, draft_building_design_uuid: str
):
    draft_building_design = DraftBuildingDesign.objects.get(
        uuid=draft_building_design_uuid
    )

    draft_building_design.status = DraftBuildingDesignStatus.CREATING_FOOTING_COMPONENTS
    draft_building_design.save()
    logger.info(
        f"Draft building design {draft_building_design_uuid} status updated to CREATING_FOOTING_COMPONENTS"
    )

    footings_drawings = DraftBuildingDesignDrawingDocument.objects.filter(
        draft_building_design=draft_building_design,
        type=DraftBuildingDesignDrawingDocumentType.FOOTING,
    )
    logger.info(
        f"Found {footings_drawings.count()} footings drawings for draft building design {draft_building_design_uuid}"
    )

    new_footing_components = []
    for drawing in footings_drawings:
        footings = extract_footings_from_image_service(
            drawing_document_uuid=drawing.uuid,
        )
        for footing in footings:
            new_footing_components.append(
                BuildingComponent(
                    type=BuildingComponentType.FOOTING,
                    component_data=footing.model_dump(),
                    description=f"Generated from drawing document {drawing.uuid}",
                )
            )

    BuildingComponent.objects.bulk_create(new_footing_components)

    for footing_component in new_footing_components:
        DraftBuildingDesign.objects.link_building_component_to_building_design(
            building_design_uuid=draft_building_design.uuid,
            building_component_uuid=footing_component.uuid,
        )

    draft_building_design.status = DraftBuildingDesignStatus.CREATING_COLUMN_COMPONENTS
    draft_building_design.save()
