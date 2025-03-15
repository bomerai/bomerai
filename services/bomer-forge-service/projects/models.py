from django.db import models
from core.base_model import AuditableBaseModel


class ProjectType(models.TextChoices):
    """
    A type of project.
    """

    STRUCTURAL_DESIGN = "STRUCTURAL_DESIGN"
    ARQUITECTURAL_DESIGN = "ARQUITECTURAL_DESIGN"


class Project(
    AuditableBaseModel,
    created_related_name="created_projects",
    updated_related_name="updated_projects",
):
    name = models.CharField(max_length=255)
    description = models.TextField()
    reference = models.CharField(max_length=255)
    type = models.CharField(
        max_length=255,
        choices=ProjectType.choices,
        default=ProjectType.STRUCTURAL_DESIGN,
    )

    def __str__(self):
        return self.name
