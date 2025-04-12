"""
This module is responsible for measuring the dimensions of the building.

It measures the length of beams or continuous footings.
"""

import structlog
import ezdxf

from draft_building_designs.models import DraftBuildingDesignDrawingDocument

logger = structlog.get_logger(__name__)


def measure_building_components_from_design_drawing_document(
    design_drawing_document: DraftBuildingDesignDrawingDocument,
) -> None:
    """
    Measure the dimensions of the building components.
    """
    dxf_file = design_drawing_document.file
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    for entity in msp:
        if entity.dxftype() == "LINE":
            print(entity.dxf.start, entity.dxf.end)
