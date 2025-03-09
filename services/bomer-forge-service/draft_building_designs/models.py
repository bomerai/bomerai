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
        draft_building_design = self.create(
            project_id=project_uuid,
        )

        return draft_building_design

    def upload_drawing_design(
        self,
        *,
        building_design_uuid: str,
        files: list[File],
        design_drawing_type: str,
        design_drawing_component_metadata_type: str,
        design_drawing_component_metadata_subtype: str,
    ):
        """
        Upload a drawing design to a draft building design.
        """
        from draft_building_designs.services.ai_drawing_component_footing_extractor import (
            extract_footings_metadata,
        )
        from draft_building_designs.services.ai_drawing_component_column_extractor import (
            extract_columns_metadata,
        )

        logger.info(
            f"Uploading drawing design for building design {building_design_uuid}"
        )
        design_drawing, _ = DesignDrawing.objects.get_or_create(
            building_design_id=building_design_uuid,
            type=DesignDrawingType(design_drawing_type),
        )

        if (
            design_drawing_component_metadata_subtype
            == DesignDrawingComponentMetadataSubtype.FOOTING
        ):
            for file in files:
                doc = DesignDrawingDocument.objects.create(
                    design_drawing=design_drawing,
                    file=file,
                    type=DesignDrawingComponentMetadataType(
                        design_drawing_component_metadata_type
                    ),
                    subtype=DesignDrawingComponentMetadataSubtype(
                        design_drawing_component_metadata_subtype
                    ),
                )
                logger.info(f"Extracting footing metadata for document {doc.uuid}")
                footings = extract_footings_metadata(
                    drawing_document_uuid=str(doc.uuid), language_code="pt"
                )
                for footing in footings:
                    design_drawing_component = (
                        DesignDrawingComponentMetadata.objects.create(
                            design_drawing=design_drawing,
                            type=DesignDrawingComponentMetadataType(
                                design_drawing_component_metadata_type
                            ),
                            subtype=DesignDrawingComponentMetadataSubtype(
                                design_drawing_component_metadata_subtype
                            ),
                            data=footing.model_dump(),
                            justification=footing.justification,
                        )
                    )

                    logger.info(f"Footing metadata: {design_drawing_component.data}")

        elif (
            design_drawing_component_metadata_subtype
            == DesignDrawingComponentMetadataSubtype.COLUMN
        ):
            for file in files:
                doc = DesignDrawingDocument.objects.create(
                    design_drawing=design_drawing,
                    file=file,
                    type=DesignDrawingComponentMetadataType(
                        design_drawing_component_metadata_type
                    ),
                    subtype=DesignDrawingComponentMetadataSubtype(
                        design_drawing_component_metadata_subtype
                    ),
                )
                logger.info(f"Extracting columns metadata for document {doc.uuid}")
                columns = extract_columns_metadata(
                    drawing_document_uuid=str(doc.uuid),
                    language_code="pt",
                )
                for column in columns:
                    design_drawing_component = (
                        DesignDrawingComponentMetadata.objects.create(
                            design_drawing=design_drawing,
                            type=DesignDrawingComponentMetadataType(
                                design_drawing_component_metadata_type
                            ),
                            subtype=DesignDrawingComponentMetadataSubtype(
                                design_drawing_component_metadata_subtype
                            ),
                        )
                    )
                    design_drawing_component.data = column.model_dump()
                    design_drawing_component.save()
                    logger.info(f"Column metadata: {design_drawing_component.data}")

    def create_design_drawing_cluster(
        self,
        *,
        building_design_uuid: str,
        design_drawing_plan_uuids: list[str],
        description: str,
    ) -> "DesignDrawingCluster":
        design_drawing_cluster = DesignDrawingCluster.objects.create(
            building_design_id=building_design_uuid,
            description=description,
        )
        design_drawing_cluster.design_drawing_plans.set(design_drawing_plan_uuids)
        design_drawing_cluster.save()

        return design_drawing_cluster


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
    PUBLISHED = "PUBLISHED"


class DraftBuildingDesign(BaseModel):
    """
    A draft building design is a design for a building that is not yet finalized.
    """

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
    quantity = models.IntegerField(default=0)


class DesignDrawingType(models.TextChoices):
    """
    A type of design drawing.
    """

    STRUCTURAL_DRAWING = "STRUCTURAL_DRAWING"
    ARQUITECTURAL_DRAWING = "ARQUITECTURAL_DRAWING"


class DesignDrawing(BaseModel):
    """
    A design drawing is a drawing of a building design.
    """

    building_design = models.ForeignKey(DraftBuildingDesign, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=DesignDrawingType.choices)

    class Meta:
        verbose_name = "Design Drawing"
        verbose_name_plural = "Design Drawings"


class DesignDrawingComponentMetadataType(models.TextChoices):
    """
    A type of component of a design drawing.
    """

    # Structural
    FOUNDATION_PLAN = "FOUNDATION_PLAN"
    FRAMING_PLAN = "FRAMING_PLAN"


class DesignDrawingComponentMetadataSubtype(models.TextChoices):
    """
    A subtype of a component of a design drawing.
    """

    # Foundation
    FOOTING = "FOOTING"

    # Framing
    COLUMN = "COLUMN"
    BEAM = "BEAM"
    SLAB = "SLAB"


class DesignDrawingComponentMetadata(BaseModel):
    """
    A metadata of a component of a design drawing.
    """

    design_drawing = models.ForeignKey(
        DesignDrawing,
        on_delete=models.CASCADE,
        related_name="design_drawing_components_metadata",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    type = models.CharField(
        max_length=255, choices=DesignDrawingComponentMetadataType.choices
    )
    subtype = models.CharField(
        max_length=255, choices=DesignDrawingComponentMetadataSubtype.choices
    )
    data = models.JSONField(null=True)
    justification = models.TextField(null=True)

    """
    The task ID for the background task that calculates BOM for a single component.
    """

    task_id = models.CharField(max_length=255, null=True)

    """
    The calculated BOM for the component.
    """

    bom = models.JSONField(null=True)

    """
    Whether the component is locked and cannot be edited.
    Once is locked, the component is used in a building design and cannot be edited.
    """

    is_locked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Design Drawing Component Metadata"
        verbose_name_plural = "Design Drawing Component Metadata"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.type} - {self.subtype}"


def upload_design_drawing_document(instance, filename):
    return f"bucket/design_drawing_documents/{str(instance.design_drawing.uuid)}/{filename}"


class DesignDrawingDocument(BaseModel):
    """
    A document of a design drawing.
    """

    design_drawing = models.ForeignKey(
        DesignDrawing, on_delete=models.CASCADE, related_name="documents"
    )
    type = models.CharField(
        max_length=255, choices=DesignDrawingComponentMetadataType.choices
    )
    subtype = models.CharField(
        max_length=255, choices=DesignDrawingComponentMetadataSubtype.choices
    )
    file = models.FileField(upload_to=upload_design_drawing_document)

    class Meta:
        verbose_name = "Design Drawing Document"
        verbose_name_plural = "Design Drawing Documents"


class DesignDrawingCluster(BaseModel):
    """
    A cluster of design drawings.
    """

    building_design = models.ForeignKey(DraftBuildingDesign, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    design_drawing_components_metadata = models.ManyToManyField(
        DesignDrawingComponentMetadata, related_name="clusters"
    )

    class Meta:
        verbose_name = "Design Drawing Cluster"
        verbose_name_plural = "Design Drawing Clusters"
