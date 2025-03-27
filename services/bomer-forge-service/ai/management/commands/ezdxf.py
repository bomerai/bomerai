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

        # get continous footing length based on the distance between the pillars
        for entity in msp.query("TEXT"):
            if entity.dxf.text[0] == "P":
                logger.info("Entity", value=entity.dxf.text, position=entity.dxf.insert)

        # Step 1: Extract footings (assuming they are LINE entities)
        footings = []
        for entity in msp.query(
            "LINE[layer=='VIG_FACES']"
        ):  # You may need to filter by layer, e.g., msp.query('LINE[layer=="FOOTINGS"]')
            start = Vec2(entity.dxf.start)  # Start point of the line
            end = Vec2(entity.dxf.end)  # End point of the line
            length = start.distance(end)  # Calculate the length of the footing
            footings.append(
                {
                    "start": start,
                    "end": end,
                    "length": length,
                    "is_horizontal": abs(start.y - end.y)
                    < 1e-3,  # Check if the line is horizontal
                    "is_vertical": abs(start.x - end.x)
                    < 1e-3,  # Check if the line is vertical
                }
            )

        # Step 2: Extract columns (assuming they are INSERT entities with associated TEXT)
        columns = []
        for insert in msp.query(
            "INSERT"
        ):  # You may need to filter by layer or block name
            # Get the insertion point of the column
            position = Vec2(insert.dxf.insert)
            # Look for nearby TEXT or MTEXT to get the column label (e.g., "P1", "P2")
            label = "Unknown"
            for text in msp.query("TEXT MTEXT").filter(
                lambda e: Vec2(e.dxf.insert).distance(position) < 5
            ):  # Adjust distance threshold as needed
                label = text.dxf.text
                break
            columns.append({"label": label, "position": position})

        # Step 3: Associate columns with footings
        footing_column_map = []
        for footing in footings:
            supported_columns = []
            if footing["is_horizontal"]:
                # For horizontal footings, check if columns are above (same y-coordinate, within x-range)
                y = footing["start"].y
                x_min = min(footing["start"].x, footing["end"].x)
                x_max = max(footing["start"].x, footing["end"].x)
                for column in columns:
                    col_x, col_y = column["position"].x, column["position"].y
                    if (
                        abs(col_y - y) < 1e-3 and x_min <= col_x <= x_max
                    ):  # Adjust tolerance as needed
                        supported_columns.append(column["label"])
            elif footing["is_vertical"]:
                # For vertical footings, check if columns are aligned (same x-coordinate, within y-range)
                x = footing["start"].x
                y_min = min(footing["start"].y, footing["end"].y)
                y_max = max(footing["start"].y, footing["end"].y)
                for column in columns:
                    col_x, col_y = column["position"].x, column["position"].y
                    if (
                        abs(col_x - x) < 1e-3 and y_min <= col_y <= y_max
                    ):  # Adjust tolerance as needed
                        supported_columns.append(column["label"])

            footing_column_map.append(
                {
                    "footing_length": footing["length"],
                    "supported_columns": supported_columns,
                }
            )

        # Step 4: Output the results
        for i, footing_info in enumerate(footing_column_map, 1):
            print(f"Footing {i}:")
            print(f"  Length: {footing_info['footing_length']:.2f} units")
            print(
                f"  Supported Columns: {', '.join(footing_info['supported_columns']) if footing_info['supported_columns'] else 'None'}"
            )
            print()
