from django.db import models

from core.base_model import BaseModel
from building_components.models import BuildingComponent
from projects.models import Project


class DraftBuildingDesignManager(models.Manager["DraftBuildingDesign"]):
    def create_draft_building_design(
        self,
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


class DesignDrawingPlanType(models.TextChoices):
    """
    A type of plan of a design drawing.
    """

    # Structural
    FOUNDATION_PLAN = "FOUNDATION_PLAN"
    FRAMING_PLAN = "FRAMING_PLAN"


class DesignDrawingPlanSubtype(models.TextChoices):
    """
    A subtype of a plan of a design drawing.
    """

    # Foundation
    FOOTING = "FOOTING"

    # Framing
    COLUMN = "COLUMN"
    BEAM = "BEAM"
    SLAB = "SLAB"


class DesignDrawingPlan(BaseModel):
    """
    A plan of a design drawing.
    """

    design_drawing = models.ForeignKey(DesignDrawing, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=DesignDrawingPlanType.choices)
    subtype = models.CharField(max_length=255, choices=DesignDrawingPlanSubtype.choices)
    plan_metadata = models.JSONField(null=True)
    documents = models.ManyToManyField(
        "draft_building_designs.DesignDrawingDocument",
        related_name="design_drawings",
    )

    class Meta:
        verbose_name = "Design Drawing Plan"
        verbose_name_plural = "Design Drawing Plans"


def upload_design_drawing_document(instance, filename):
    return f"design_drawing_documents/{instance.design_drawing_plan.id}/{filename}"


class DesignDrawingDocument(BaseModel):
    """
    A document of a design drawing.
    """

    design_drawing_plan = models.ForeignKey(DesignDrawingPlan, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_design_drawing_document)

    class Meta:
        verbose_name = "Design Drawing Document"
        verbose_name_plural = "Design Drawing Documents"
