from django.db import models

from core.base_model import BaseModel
from treebeard.mp_tree import MP_Node
import structlog

logger = structlog.get_logger(__name__)


class BuildingComponentType(models.TextChoices):
    """
    A building component type is a type of building component.
    """

    FOOTING = "FOOTING"
    COLUMN = "COLUMN"
    BEAM = "BEAM"
    SLAB = "SLAB"


class BuildingComponent(BaseModel):
    """
    A building component is a part of a building design.
    It can be a wall, floor, ceiling, door, window, etc.
    """

    description = models.TextField(blank=True, null=True)
    component_data = models.JSONField(
        help_text="The data for the component",
        null=True,
        blank=True,
    )
    type = models.CharField(max_length=255, choices=BuildingComponentType.choices)

    def __str__(self):
        """Return a string representation of the building component."""
        return f"{str(self.type)} - {self.description}"


class BuildingComponentEvaluation(BaseModel):
    """
    A building component evaluation is a evaluation of a building component.
    """

    building_component = models.ForeignKey(BuildingComponent, on_delete=models.CASCADE)
    evaluation_data = models.JSONField(
        help_text="The data for the evaluation",
        null=True,
        blank=True,
    )
    rationale = models.TextField(
        help_text="The rationale for the evaluation",
        null=True,
        blank=True,
    )
