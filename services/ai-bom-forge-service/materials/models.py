from django.db import models
from core.base_model import BaseModel


class Material(BaseModel):
    """
    A material is a material that is used in a building component.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    dimensions = models.JSONField(
        help_text="The dimensions of the material",
        null=True,
        blank=True,
    )
    metadata = models.JSONField(
        help_text="The metadata for the material",
        null=True,
        blank=True,
    )
