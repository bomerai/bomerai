from django.db import models

from core.base_model import BaseModel, TimestampedModel
from django.contrib.auth.models import User
from building_components.models import BuildingComponent
from materials.models import Material
from draft_building_designs.tasks import ai_generate_building_design_from_prompt


class DraftBuildingDesignKind(models.TextChoices):
    HOUSE = "HOUSE"
    BUILDING = "BUILDING"


class DraftBuildingDesignManager(models.Manager["DraftBuildingDesign"]):
    def create_draft_building_design(
        self,
        name: str,
        description: str,
        kind: DraftBuildingDesignKind,
        address: str,
        owner: User,
    ) -> "DraftBuildingDesign":
        draft_building_design = self.create(
            name=name,
            description=description,
            kind=kind,
            address=address,
            owner=owner,
        )
        ai_generate_building_design_from_prompt.delay(
            draft_building_design.uuid,
        )
        return draft_building_design


class DraftBuildingDesign(TimestampedModel):
    """
    A draft building design is a design for a building that is not yet finalized.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    kind = models.CharField(max_length=255, choices=DraftBuildingDesignKind.choices)
    address = models.TextField(default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    objects: DraftBuildingDesignManager = DraftBuildingDesignManager()


class UnitOfMeasure(models.TextChoices):
    METERS = "METERS"
    SQUARE_METERS = "SQUARE_METERS"
    CUBIC_METERS = "CUBIC_METERS"
    LITERS = "LITERS"
    KILOGRAMS = "KILOGRAMS"
    UNIT = "UNIT"


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


class DraftBuildingDesignBuildingComponentMaterial(BaseModel):
    """
    A building component material is a material that is used in a building component.
    """

    draft_building_design_building_component = models.ForeignKey(
        DraftBuildingDesignBuildingComponent, on_delete=models.CASCADE
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
