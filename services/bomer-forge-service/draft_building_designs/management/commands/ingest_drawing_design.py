import os
import io
import ezdxf
import structlog
from django.core.management.base import BaseCommand
from draft_building_designs.models import DXFEntity, DraftBuildingDesign
from pydantic import BaseModel
from ezdxf.math import Vec3
from ezdxf.lldxf.tagwriter import TagWriter
from ezdxf.entities.factory import ENTITY_CLASSES
from ezdxf.entities import polyline
import json

logger = structlog.get_logger(__name__)


class Entity(BaseModel):
    text: str | None = None
    coordinates: tuple[float, float] | list[tuple[float, float]]
    layer: str
    dxftype: str


class Command(BaseCommand):
    help = "Ingest a drawing design"

    def handle(self, *args, **kwargs):
        draft_building_design = DraftBuildingDesign.objects.first()

        doc = ezdxf.readfile(
            os.path.join(os.path.dirname(__file__), "projeto de estrutura.dxf")
        )
        msp = doc.modelspace()

        dxfentities: list[DXFEntity] = []

        for entity in msp:
            entity_type = entity.dxftype()
            stream = io.StringIO()
            entity.export_dxf(TagWriter(stream))
            logger.info("Entity", entity_serialized=str(stream.getvalue()))
            stream.close()

            continue
            match entity_type:
                case "LINE":
                    entity = Entity(
                        text=None,
                        coordinates=[
                            (entity.dxf.start.x, entity.dxf.start.y),
                            (entity.dxf.end.x, entity.dxf.end.y),
                        ],
                        layer=entity.dxf.layer,
                        dxftype="LINE",
                    )

                case "TEXT":
                    entity = Entity(
                        text=entity.dxf.text,
                        coordinates=(entity.dxf.insert.x, entity.dxf.insert.y),
                        layer=entity.dxf.layer,
                        dxftype="TEXT",
                    )
                case "MTEXT":
                    entity = Entity(
                        text=entity.dxf.text,
                        coordinates=(entity.dxf.insert.x, entity.dxf.insert.y),
                        layer=entity.dxf.layer,
                        dxftype="MTEXT",
                    )
                case "DIMENSION":
                    entity = Entity(
                        text=entity.dxf.text,
                        coordinates=(entity.dxf.defpoint.x, entity.dxf.defpoint.y),
                        layer=entity.dxf.layer,
                        dxftype="DIMENSION",
                    )
                case "POLYLINE":
                    coordinates = []
                    for vertex in entity.vertices:
                        coordinates.append(
                            (vertex.dxf.location.x, vertex.dxf.location.y)
                        )
                    entity = Entity(
                        text=None,
                        coordinates=coordinates,
                        layer=entity.dxf.layer,
                        dxftype="POLYLINE",
                    )
                case _:
                    continue

            dxfentities.append(
                DXFEntity(
                    draft_building_design=draft_building_design,
                    metadata=entity.model_dump(),
                    tags=[entity.dxftype],
                )
            )
            logger.info(
                f"Ingested {entity.text} - {entity.coordinates} - {entity.dxftype}"
            )

        DXFEntity.objects.bulk_create(dxfentities)
