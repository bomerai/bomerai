import uuid

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    Base model for all models in the project.
    """

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimestampedBaseModel(BaseModel):
    """
    Timestamped model for all models in the project.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditableBaseModel(BaseModel):
    """
    Auditabled model for all models in the project.
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __init_subclass__(
        cls: type["AuditableBaseModel"],
        created_related_name: str | None = None,
        updated_related_name: str | None = None,
        **kwargs: dict,
    ) -> None:
        """Customize subclass initialization.

        This method allows the dynamic setting of `related_name` attributes
        for the `created_by` and `updated_by` fields in subclasses of
        `AuditableBaseModel`. It ensures that each subclass can have unique
        reverse relation names.
        """
        super().__init_subclass__(**kwargs)

        created_field = cls._meta.get_field("created_by")
        if isinstance(created_field.remote_field, models.ForeignObjectRel):
            created_field.remote_field.related_name = created_related_name

        # Modify the 'updated_by' field's related_name if it exists and is a ForeignObjectRel
        updated_field = cls._meta.get_field("updated_by")
        if isinstance(updated_field.remote_field, models.ForeignObjectRel):
            updated_field.remote_field.related_name = updated_related_name


class UnitOfMeasure(models.TextChoices):
    METERS = "METERS"
    CENTIMETERS = "CENTIMETERS"
    MILLIMETERS = "MILLIMETERS"
    SQUARE_METERS = "SQUARE_METERS"
    CUBIC_METERS = "CUBIC_METERS"
    LITERS = "LITERS"
    KILOGRAMS = "KILOGRAMS"
    UNIT = "UNIT"
