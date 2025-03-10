from django.db import models
from core.base_model import BaseModel
from django.core.files.base import File
from draft_building_designs.models import DraftBuildingDesign


def upload_building_design_evaluation_file(instance, filename):
    return (
        f"building_design_evaluations/{instance.draft_building_design.uuid}/{filename}"
    )


class BuildingDesignEvaluation(BaseModel):
    """
    A building design evaluation is a evaluation of a building design
    from a given blueprint uploaded by the user.
    """

    draft_building_design = models.ForeignKey(
        DraftBuildingDesign,
        on_delete=models.CASCADE,
        related_name="evaluations",
    )

    file = models.FileField(upload_to=upload_building_design_evaluation_file)
