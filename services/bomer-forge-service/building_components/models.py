from django.db import models
from pgvector.django import VectorField

from core.base_model import UnitOfMeasure, BaseModel, AuditableBaseModel
from materials.models import Material


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


class BuildingComponentSourceStudy(models.Model):
    building_component = models.ForeignKey(
        "building_components.BuildingComponent", on_delete=models.CASCADE
    )
    study = models.ForeignKey("studies.Study", on_delete=models.CASCADE)

    class Meta:
        """Meta options for the BuildingComponentSourceStudy model."""

        unique_together = ("building_component", "study")
        indexes = (models.Index(fields=["study"], name="study_idx"),)

    def __str__(self):
        """Return a string representation of the BuildingComponentSourceStudy."""
        return f"{self.study.name}, {self.building_component}"


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

    def link_material_to_building_component(
        self,
        building_component_uuid: str,
        material_uuid: str,
        quantity: int,
        unit: UnitOfMeasure,
        justification: str,
    ) -> "BuildingComponentMaterial":
        building_component = BuildingComponent.objects.get(uuid=building_component_uuid)
        material = Material.objects.get(uuid=material_uuid)

        return BuildingComponentMaterial.objects.update_or_create(
            building_component=building_component,
            material=material,
            quantity=quantity,
            unit=unit,
            justification=justification,
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

    source_studies = models.ManyToManyField(
        "studies.Study",
        through=BuildingComponentSourceStudy,
        related_name="building_components",
    )

    materials = models.ManyToManyField(
        Material,
        related_name="building_components",
        through="building_components.BuildingComponentMaterial",
    )

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


class BuildingComponentMaterial(BaseModel):
    """
    A building component material is a material that is used in a building component.
    """

    building_component = models.ForeignKey(BuildingComponent, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=255, choices=UnitOfMeasure.choices)
    justification = models.TextField(default="")
