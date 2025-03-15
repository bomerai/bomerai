from django.db import models

from core.base_model import BaseModel
from treebeard.mp_tree import MP_Node


class BuildingComponentType(MP_Node):
    """
    A building component type is a type of building component.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Return a string representation of the building component type."""
        return f"{self.name} - {self.description}"


class BuildingComponent(BaseModel):
    """
    A building component is a part of a building design.
    It can be a wall, floor, ceiling, door, window, etc.
    """

    description = models.TextField(blank=True)
    component_data = models.JSONField(
        help_text="The data for the component",
        null=True,
        blank=True,
    )
    type = models.ForeignKey(
        BuildingComponentType,
        on_delete=models.CASCADE,
        related_name="building_components",
    )

    def __str__(self):
        """Return a string representation of the building component."""
        return f"{self.type.name} - {self.description}"


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
