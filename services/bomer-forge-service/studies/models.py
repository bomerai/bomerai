from typing import TypedDict

from django.contrib.postgres.fields import ArrayField
from django.db import models

from building_components.models import BuildingComponent
from core.base_model import BaseModel
from draft_building_designs.models import DraftBuildingDesign


class SimilarStudy(TypedDict):
    study: "Study"
    similarity_score: float


class StudyManager(models.Manager["Study"]):
    def get_similar_studies_for_draft_building_design(
        self,
        *,
        draft_building_design: DraftBuildingDesign,
        min_num_studies_to_return: int = 1,
        similarity_score_threshold: int = 80,
    ) -> list[SimilarStudy]:
        """Return a list of similar studies to the given study.
        The similarity is calculated based on the building design, the requirements and the summary.
        """
        return []


class Study(BaseModel):
    """
    This model represents a study.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    summary = models.TextField()
    building_design = models.JSONField(null=True)
    requirements = ArrayField(models.CharField(max_length=1024), null=True)

    # type hinting for the building_components field
    building_components = models.QuerySet["BuildingComponent"]

    objects: StudyManager = StudyManager()
