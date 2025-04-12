import os

import ezdxf
import json
import structlog
from django.core.management.base import BaseCommand
from ezdxf.math import Vec2
from pydantic import BaseModel
from ai.services.runnables import get_gpt, get_langfuse_callback_handler

logger = structlog.get_logger(__name__)


identifiers = {
    "BEAM_1": "VIG_FACES",
}


class Command(BaseCommand):
    help = "Print all layers in a DXF file"

    def handle(self, *args, **kwargs):
        doc = ezdxf.readfile(
            os.path.join(os.path.dirname(__file__), "projeto de estrutura.dxf")
        )
        logger.info(
            "Document loaded",
            doc=doc,
        )
        msp = doc.modelspace()

        # vectors = []
        # get continous footing length based on the distance between the pillars
        # for entity in msp.query("LINE[layer=='VIG_FACES']"):
        #     v1 = entity.dxf.start
        #     v2 = entity.dxf.end
        #     coordinates = [v1.x, v1.y, v2.x, v2.y]
        #     vectors.append(coordinates)

        # logger.info("Vectors", vectors=vectors)
        # with open("vectors.json", "w") as f:
        #     json.dump(vectors, f)

        gpt = get_gpt()

        for entity in msp.query("TEXT"):
            logger.info("Entity", text=entity.dxf.text)
