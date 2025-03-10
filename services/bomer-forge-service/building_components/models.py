from django.db import models
from pgvector.django import VectorField

from core.base_model import UnitOfMeasure, BaseModel


class BuildingComponentType(models.TextChoices):
    FOUNDATION = "FOUNDATION"
    FRAMING = "FRAMING"


class BuildingComponentSubtype(models.TextChoices):
    FOOTING = "FOOTING"
    COLUMN = "COLUMN"
    BEAM = "BEAM"
    SLAB = "SLAB"
    WALL = "WALL"
    FLOOR = "FLOOR"
    CEILING = "CEILING"
    ROOF = "ROOF"


class BuildingComponentManager(models.Manager["BuildingComponent"]):
    def create_exterior_wall_component(
        self,
        description: str,
        dimensions: dict,
        component_data: dict,
        unit_of_measure: UnitOfMeasure,
    ) -> "BuildingComponent":
        return BuildingComponent.objects.create(
            description=description,
            dimensions=dimensions,
            component_data=component_data,
            unit_of_measure=unit_of_measure,
            type=BuildingComponentType.WALL,
            subtype=BuildingComponentSubtype.EXTERIOR,
        )


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
    embedding_vector = VectorField(
        help_text="The embedding vector for the component",
        null=True,
        blank=True,
        dimensions=1536,
    )
    type = models.CharField(max_length=255, choices=BuildingComponentType.choices)
    subtype = models.CharField(max_length=255, choices=BuildingComponentSubtype.choices)

    objects: BuildingComponentManager = BuildingComponentManager()

    def __str__(self):
        """Return a string representation of the building component."""
        return f"{self.type}:{self.subtype} - {self.description}"

    def get_area(self) -> tuple[float, UnitOfMeasure]:
        """Return the area of the building component."""
        length = self.dimensions.get("length", 0)
        width = self.dimensions.get("width", 0)
        height = self.dimensions.get("height", 0)

        area = 0
        match self.type:
            case BuildingComponentType.WALL:
                area = length * height
            case BuildingComponentType.FLOOR:
                area = length * width
            case _:
                raise ValueError(f"Unsupported building component type: {self.type}")

        unit = UnitOfMeasure(self.dimensions.get("unit"))
        match unit:
            case UnitOfMeasure.METERS:
                return area, UnitOfMeasure.SQUARE_METERS
            case UnitOfMeasure.CENTIMETERS:
                return area / 10000, UnitOfMeasure.SQUARE_METERS
            case UnitOfMeasure.MILLIMETERS:
                return area / 1000000, UnitOfMeasure.SQUARE_METERS
            case _:
                raise ValueError(f"Unsupported unit of measure: {unit}")
