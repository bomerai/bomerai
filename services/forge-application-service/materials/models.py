from django.db import models
from core.base_model import BaseModel


class UnitOfMeasure(models.TextChoices):
    METERS = "METERS"
    SQUARE_METERS = "SQUARE_METERS"
    CUBIC_METERS = "CUBIC_METERS"
    LITERS = "LITERS"
    KILOGRAMS = "KILOGRAMS"
    UNIT = "UNIT"


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
    unit_of_measure = models.CharField(max_length=255, choices=UnitOfMeasure.choices)
    cost_per_unit_of_measure = models.PositiveIntegerField(
        help_text="Cost per unit in cents (integer)",
    )
    quantity = models.PositiveIntegerField(
        help_text="Quantity of the material",
    )
