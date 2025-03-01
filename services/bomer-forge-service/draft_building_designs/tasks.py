from celery import shared_task
import structlog
from draft_building_designs.services.ai_building_design_generation import (
    generate_building_design_components as generate_building_design_components_func,
)

logger = structlog.get_logger(__name__)


@shared_task
def generate_building_design_components(
    draft_building_design_uuid: str,
):
    """Generate a building design components for a draft building design"""
    logger.info(
        f"Generating building design components with uuid {draft_building_design_uuid}",
    )
    generate_building_design_components_func(
        draft_building_design_uuid=draft_building_design_uuid
    )
