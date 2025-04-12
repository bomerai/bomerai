import structlog
from django.db import models

from building_components.models import BuildingComponent
from core.base_model import BaseModel
from projects.models import Project
from pgvector.django import VectorField

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

    def link_building_component_to_building_design(
        self,
        *,
        building_design_uuid: str,
        building_component_uuid: str,
    ):
        """
        Link a building component to a building design.
        """
        building_design = DraftBuildingDesign.objects.get(uuid=building_design_uuid)
        building_component = BuildingComponent.objects.get(uuid=building_component_uuid)
        DraftBuildingDesignBuildingComponent.objects.create(
            draft_building_design=building_design,
            building_component=building_component,
        )


class DraftBuildingDesignStatus(models.TextChoices):
    """
    A status of a draft building design.
    """

    NOT_STARTED = "NOT_STARTED"
    CREATING_FOOTING_COMPONENTS = "CREATING_FOOTING_COMPONENTS"
    CREATING_COLUMN_COMPONENTS = "CREATING_COLUMN_COMPONENTS"
    CREATING_BEAM_COMPONENTS = "CREATING_BEAM_COMPONENTS"
    CREATING_SLAB_COMPONENTS = "CREATING_SLAB_COMPONENTS"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class DraftBuildingDesign(BaseModel):
    """
    A draft building design is a design for a building that is not yet finalized.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="draft_building_designs"
    )
    status = models.CharField(
        max_length=255,
        choices=DraftBuildingDesignStatus.choices,
        default=DraftBuildingDesignStatus.CREATING_FOOTING_COMPONENTS,
    )
    building_components = models.ManyToManyField(
        BuildingComponent,
        related_name="draft_building_designs",
        through="draft_building_designs.DraftBuildingDesignBuildingComponent",
    )

    objects: DraftBuildingDesignManager = DraftBuildingDesignManager()

    def __str__(self):
        return f"{self.name} - {self.project.name}"


def get_draft_building_design_drawing_document_upload_path(
    instance: "DraftBuildingDesignDrawingDocument", filename: str
) -> str:
    return f"bucket/draft_building_designs/{instance.draft_building_design.uuid}/drawing_documents/{filename}"


class DraftBuildingDesignCalculationModuleType(models.TextChoices):
    """
    A type of draft building design calculation module.
    """

    STRUCTURE_PROJECT = "STRUCTURE_PROJECT"


class DraftBuildingDesignCalculationModuleStatus(models.TextChoices):
    """
    A status of a draft building design calculation module.
    """

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class DraftBuildingDesignCalculationModule(BaseModel):
    """
    A draft building design calculation module is a module for a building design.
    """

    draft_building_design = models.ForeignKey(
        DraftBuildingDesign,
        on_delete=models.CASCADE,
        related_name="calculation_modules",
    )
    status = models.CharField(
        max_length=255,
        choices=DraftBuildingDesignCalculationModuleStatus.choices,
        default=DraftBuildingDesignCalculationModuleStatus.NOT_STARTED,
    )
    type = models.CharField(
        max_length=255,
        choices=DraftBuildingDesignCalculationModuleType.choices,
        default=DraftBuildingDesignCalculationModuleType.STRUCTURE_PROJECT,
    )


class DraftBuildingDesignDrawingDocumentType(models.TextChoices):
    """
    A type of drawing document.
    """

    FOOTING = "FOOTING"
    COLUMN = "COLUMN"
    BEAM = "BEAM"
    SLAB = "SLAB"


class DraftBuildingDesignDrawingDocument(BaseModel):
    """
    A drawing document is a document that is part of a building design.
    """

    draft_building_design = models.ForeignKey(
        DraftBuildingDesign, on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=get_draft_building_design_drawing_document_upload_path
    )
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=255,
        choices=DraftBuildingDesignDrawingDocumentType.choices,
        default=DraftBuildingDesignDrawingDocumentType.FOOTING,
    )


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


class DXFEntity(BaseModel):
    """
    A DXF entity is an entity in a DXF file.
    """

    draft_building_design = models.ForeignKey(
        DraftBuildingDesign, on_delete=models.CASCADE, related_name="dxf_entities"
    )
    metadata = models.JSONField(
        help_text="Metadata of the entity in the DXF file",
        null=True,
        blank=True,
    )
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    tags = models.JSONField(
        help_text="Array of tags of the element in the DXF file", null=True, blank=True
    )

    class Meta:
        verbose_name = "DXF Entity"
        verbose_name_plural = "DXF Entities"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.draft_building_design.name} - {self.metadata}"
