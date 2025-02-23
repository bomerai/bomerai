from django.db import models
from pgvector.django import VectorField

from core.base_model import TimestampedModel, UnitOfMeasure


class BuildingComponentType(models.TextChoices):
    WALL = "WALL"
    FLOOR = "FLOOR"
    CEILING = "CEILING"
    ROOF = "ROOF"
    DOOR = "DOOR"
    WINDOW = "WINDOW"


class BuildingComponentSubtype(models.TextChoices):
    EXTERIOR = "EXTERIOR"
    INTERIOR = "INTERIOR"


class BuildingComponentManager(models.Manager["BuildingComponent"]):
    def create_exterior_wall_component(
        self,
        description: str,
        dimensions: dict,
        component_data: dict,
        unit_of_measure: UnitOfMeasure,
    ) -> "BuildingComponent":
        return self.create(
            description=description,
            dimensions=dimensions,
            component_data=component_data,
            unit_of_measure=unit_of_measure,
            type=BuildingComponentType.WALL,
            subtype=BuildingComponentSubtype.EXTERIOR,
        )


class BuildingComponent(TimestampedModel):
    """
    A building component is a part of a building design.
    It can be a wall, floor, ceiling, door, window, etc.
    """

    description = models.TextField(blank=True)
    dimensions = models.JSONField(help_text="The dimensions of the component")
    component_data = models.JSONField(
        help_text="The data for the component",
        null=True,
        blank=True,
    )
    embedding_vector = VectorField(
        help_text="The embedding vector for the component",
        null=True,
        blank=True,
        dimensions=1536,
    )
    type = models.CharField(max_length=255, choices=BuildingComponentType.choices)
    subtype = models.CharField(max_length=255, choices=BuildingComponentSubtype.choices)
    unit_of_measure = models.CharField(max_length=255, choices=UnitOfMeasure.choices)

    objects: BuildingComponentManager = BuildingComponentManager()
