from django.db import models
from core.base_model import AuditableBaseModel


class Project(
    AuditableBaseModel,
    created_related_name="created_projects",
    updated_related_name="updated_projects",
):
    name = models.CharField(max_length=255)
    description = models.TextField()
    reference = models.CharField(max_length=255)

    def __str__(self):
        return self.name
