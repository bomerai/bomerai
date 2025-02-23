import uuid

from django.db import models
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(models.Model):
    """
    Base model for all models in the project.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class TimestampedModel(BaseModel):
    """
    Timestamped model for all models in the project.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UnitOfMeasure(models.TextChoices):
    METERS = "METERS"
    SQUARE_METERS = "SQUARE_METERS"
    CUBIC_METERS = "CUBIC_METERS"
    LITERS = "LITERS"
    KILOGRAMS = "KILOGRAMS"
    UNIT = "UNIT"
