from django.db import models

from core.base_model import BaseModel, TimestampedBaseModel
from django.contrib.auth.models import User
from building_components.models import BuildingComponent
from projects.models import Project


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
        from draft_building_designs.tasks import generate_building_design_components

        draft_building_design = self.create(
            name=name,
            description=description,
            kind=kind,
            address=address,
            owner=owner,
        )
        generate_building_design_components.delay(
            draft_building_design_uuid=draft_building_design.uuid,
        )
        return draft_building_design


class DraftBuildingDesign(TimestampedBaseModel):
    """
    A draft building design is a design for a building that is not yet finalized.
    """

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="draft_building_designs"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    kind = models.CharField(max_length=255, choices=DraftBuildingDesignKind.choices)
    address = models.TextField(default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

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
