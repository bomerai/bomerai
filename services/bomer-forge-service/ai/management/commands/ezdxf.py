import os

import ezdxf
import structlog
from django.core.management.base import BaseCommand
from ezdxf.math import Vec2
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


identifiers = {
    "BEAM_1": "VIG_FACES",
}


class DXFEntity(BaseModel):
    layer: str
    linetype: str
    dxftype: str


# Tolerance for comparing coordinates and lengths (to account for floating-point precision)
COORDINATE_TOLERANCE = 0.01  # For X or Y coordinates to be considered the same
LENGTH_TOLERANCE = 0.01  # For lengths to be considered the same


def extract_beams(msp):
    # Step 1: Extract all lines from the "VIGA" layer and classify them as horizontal or vertical
    horizontal_lines = []
    vertical_lines = []

    for entity in msp.query("LINE[layer=='VIG_FACES']"):
        start_point = entity.dxf.start
        end_point = entity.dxf.end

        # Calculate the 2D length of the line
        length = start_point.distance(end_point)

        # Determine if the line is horizontal or vertical
        # Horizontal: start.y == end.y (within tolerance)
        # Vertical: start.x == end.x (within tolerance)
        line_info = {
            "start": (start_point[0], start_point[1]),
            "end": (end_point[0], end_point[1]),
            "length": length,
            "entity": entity,
            "thickness": entity.dxf.thickness,
        }

        if abs(start_point[1] - end_point[1]) < COORDINATE_TOLERANCE:
            # Horizontal line (same Y)
            line_info["x"] = start_point[0]  # Use the Y-coordinate for comparison
            line_info["y"] = start_point[
                1
            ]  # Used to compute the distance between two horizontal lines
            horizontal_lines.append(line_info)
        elif abs(start_point[0] - end_point[0]) < COORDINATE_TOLERANCE:
            # Vertical line (same X)
            line_info["y"] = start_point[1]  # Use the X-coordinate for comparison
            line_info["x"] = start_point[
                0
            ]  # Used to compute the distance between two vertical lines
            vertical_lines.append(line_info)
        else:
            # Skip lines that are neither horizontal nor vertical
            print(
                f"Skipping non-horizontal/vertical line: Start = {line_info['start']}, End = {line_info['end']}"
            )
    logger.info(f"Found {len(horizontal_lines)} horizontal lines")
    logger.info(f"Found {len(vertical_lines)} vertical lines")

    # Step 2: Find pairs of horizontal lines with the same Y-coordinate and same length
    horizontal_pairs = []
    for i in range(len(horizontal_lines)):
        for j in range(i + 1, len(horizontal_lines)):
            line1 = horizontal_lines[i]
            line2 = horizontal_lines[j]
            # Check if they are on the same Y-coordinate and have the same length
            if (
                abs(line1["x"] - line2["x"]) < COORDINATE_TOLERANCE
                and abs(line1["length"] - line2["length"]) < LENGTH_TOLERANCE
            ):
                horizontal_pairs.append((line1, line2))

    # Step 3: Find pairs of vertical lines with the same X-coordinate and same length
    vertical_pairs = []
    for i in range(len(vertical_lines)):
        for j in range(i + 1, len(vertical_lines)):
            line1 = vertical_lines[i]
            line2 = vertical_lines[j]
            # Check if they are on the same X-coordinate and have the same length
            if (
                abs(line1["y"] - line2["y"]) < COORDINATE_TOLERANCE
                and abs(line1["length"] - line2["length"]) < LENGTH_TOLERANCE
            ):
                vertical_pairs.append((line1, line2))

    # Getting the beams C 2.1.0
    vigas_c_2_1_0 = []
    for pair in horizontal_pairs:
        line1, line2 = pair
        distance = (abs(line1["y"] - line2["y"]) + line1["thickness"]) * 100
        if distance > 39 and distance <= 40:
            vigas_c_2_1_0.append(pair)

    logger.info(f"Found {len(vigas_c_2_1_0)} beams C 2.1.0")


class Command(BaseCommand):
    help = "Print all layers in a DXF file"

    def handle(self, *args, **kwargs):
        doc = ezdxf.readfile(os.path.join(os.path.dirname(__file__), "fundacao.dxf"))
        logger.info(
            "Document loaded",
            doc=doc,
        )
        msp = doc.modelspace()
        # extract_beams(msp)
        for entity in msp.query("POLYLINE"):
            logger.info(f"Processing entity {entity.dxf.layer}")
            for vertex in entity.vertices:
                logger.info(f"Vertex: {vertex}")
