from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.base_model import BaseModel


class BuildingDesignEvaluation(BaseModel):
    building_design = models.ForeignKey(
        "draft_building_designs.DraftBuildingDesign",
        on_delete=models.CASCADE,
        related_name="building_design_evaluations",
    )

    # Generic Foreign Key fields
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.UUIDField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
