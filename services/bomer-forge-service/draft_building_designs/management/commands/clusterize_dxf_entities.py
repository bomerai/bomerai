import numpy as np
from django.core.management.base import BaseCommand
from sklearn.cluster import DBSCAN

from draft_building_designs.models import DXFEntity


def get_dxf_entity_point(dxf_entity: DXFEntity) -> tuple[float, float] | None:
    match dxf_entity.metadata.get("type"):
        case "POLYLINE":
            return np.mean(dxf_entity.metadata["coordinates"], axis=0)
        case "LINE":
            return np.array(dxf_entity.metadata["coordinates"])
        case _:
            return None


def clusterize_dxf_entities(dxfentities: list[DXFEntity]) -> list[DXFEntity]:
    points = np.array(
        [[entity.metadata["x"], entity.metadata["y"]] for entity in dxfentities]
    )
    dbscan = DBSCAN(eps=10, min_samples=2, metric="cosine")
    dbscan.fit(points)
    return dbscan.labels_


class Command(BaseCommand):
    help = "Clusterize DXF entities"

    def handle(self, *args, **kwargs):
        clusterize_dxf_entities(DXFEntity.objects.all())
