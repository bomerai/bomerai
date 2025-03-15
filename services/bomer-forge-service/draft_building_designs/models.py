import structlog
from django.core.files.base import File
from django.db import models

from building_components.models import BuildingComponent
from core.base_model import BaseModel
from projects.models import Project

logger = structlog.get_logger(__name__)


class DraftBuildingDesignManager(models.Manager["DraftBuildingDesign"]):
    def create_draft_building_design(
        self,
        *,
        project_uuid: str,
        name: str,
        description: str,
    ) -> "DraftBuildingDesign":
        """
        Create a draft building design.
        """
        draft_building_design = DraftBuildingDesign.objects.create(
            project_id=project_uuid,
            name=name,
            description=description,
        )

        return draft_building_design

    def upload_drawing_design(
        self,
        *,
        building_design_uuid: str,
        files: list[File],
        design_drawing_component_metadata_type: str,
        design_drawing_component_metadata_subtype: str,
        is_strip_footing: bool,
        strip_footing_length: int | None = None,
    ):
        """
        Upload a drawing design to a draft building design.
        """
        from draft_building_designs.services.ai_building_component_extraction import (
            extract_footings_from_drawing_design_document,
            extract_columns_from_drawing_design_document,
        )

        logger.info(
            f"Uploading drawing design for building design {building_design_uuid}"
        )

    def link_building_component_to_building_design(
        self,
        *,
        building_design_uuid: str,
        building_component_uuid: str,
        justification: str,
    ):
        """
        Link a building component to a building design.
        """
        building_design = DraftBuildingDesign.objects.get(uuid=building_design_uuid)
        building_component = BuildingComponent.objects.get(uuid=building_component_uuid)
        DraftBuildingDesignBuildingComponent.objects.create(
            draft_building_design=building_design,
            building_component=building_component,
            justification=justification,
        )


class DraftBuildingDesignPhase(models.TextChoices):
    """
    A phase of a draft building design.
    """

    PHASE_1 = "PHASE_1"  # BOM for the structure
    PHASE_2 = "PHASE_2"
    PHASE_3 = "PHASE_3"


class DraftBuildingDesignStatus(models.TextChoices):
    """
    A status of a draft building design.
    """

    DRAFT = "DRAFT"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class DraftBuildingDesign(BaseModel):
    """
    A draft building design is a design for a building that is not yet finalized.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="draft_building_designs"
    )
    phase = models.CharField(
        max_length=255,
        choices=DraftBuildingDesignPhase.choices,
        default=DraftBuildingDesignPhase.PHASE_1,
    )
    status = models.CharField(
        max_length=255,
        choices=DraftBuildingDesignStatus.choices,
        default=DraftBuildingDesignStatus.DRAFT,
    )
    building_components = models.ManyToManyField(
        BuildingComponent,
        related_name="draft_building_designs",
        through="draft_building_designs.DraftBuildingDesignBuildingComponent",
    )

    objects: DraftBuildingDesignManager = DraftBuildingDesignManager()


class DraftBuildingDesignBuildingComponent(BaseModel):
    """
    A building component is a part of a building design.
    """

    draft_building_design = models.ForeignKey(
        DraftBuildingDesign, on_delete=models.CASCADE
    )
    building_component = models.OneToOneField(
        BuildingComponent, on_delete=models.CASCADE
    )
    justification = models.TextField(default="")
    task_id = models.CharField(max_length=255, null=True, blank=True)
    bom = models.JSONField(null=True, blank=True)
