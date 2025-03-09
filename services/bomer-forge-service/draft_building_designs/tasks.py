from celery import shared_task
import structlog
from draft_building_designs.models import (
    DesignDrawingComponentMetadata,
    DesignDrawingComponentMetadataSubtype,
)
from draft_building_designs.services.ai_drawing_component_footing_bom_calculator import (
    calculate_bom_per_footing,
)

logger = structlog.get_logger(__name__)


@shared_task(bind=True, acks_late=True, max_retries=3)
def ai_calculate_design_drawing_component_bom(
    self,
    *,
    design_drawing_component_metadata_uuid: str,
):
    """Calculate the bill of materials for a design drawing component"""
    import time

    logger.info(
        f"Calculating bill of materials for {design_drawing_component_metadata_uuid}"
    )
    drawing_component_metadata = DesignDrawingComponentMetadata.objects.get(
        uuid=design_drawing_component_metadata_uuid
    )

    try:
        response = None
        match DesignDrawingComponentMetadataSubtype(drawing_component_metadata.subtype):
            case DesignDrawingComponentMetadataSubtype.FOOTING:
                response = calculate_bom_per_footing(
                    design_drawing_component_metadata_uuid=design_drawing_component_metadata_uuid
                )

            case _:
                raise ValueError(
                    f"Unsupported design drawing component metadata subtype: {drawing_component_metadata.uuid}"
                )

        drawing_component_metadata.bom = response.model_dump() if response else None
        drawing_component_metadata.save()
        logger.info(
            f"Successfully calculated bill of materials for {design_drawing_component_metadata_uuid}",
            response=response,
        )
    except Exception as e:
        logger.error(
            f"Error calculating bill of materials for {design_drawing_component_metadata_uuid}",
            error=e,
        )
        self.retry(exc=e)
