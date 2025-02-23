from pathlib import Path
import json
from typing import cast
from collections import defaultdict
import structlog
from pydantic import BaseModel, Field

from ai.services.runnables import get_gpt, langchain_prompt_from_text
from building_components.models import BuildingComponent, BuildingComponentType

logger = structlog.get_logger(__name__)

wall_definition = """It's a wall symbol from a floor plan, consisting of a vertical rectangle with diagonal hatching lines inside, flanked by small dots evenly distributed on both sides of the rectangle."""


# -


class ExternalWallName(BaseModel):
    name: str = Field(description="The name of the wall")


class ExternalWall(BaseModel):
    length: float = Field(description="The length of the wall")
    angle: float = Field(description="The angle of the wall")


class Material(BaseModel):
    name: str = Field(description="The name of the material")
    description: str = Field(description="The description of the material")
    retail_price: dict = Field(
        description="The unit price of the material",
        examples=[
            {"value": 10, "unit": "USD/m²"},
            {"value": 10, "unit": "USD/kg"},
            {"value": 0, "unit": "USD/m³"},
        ],
    )
    material_metadata: dict = Field(
        description="The metadata of the material",
        example={
            "properties": {
                "component_types": ["wall"],
                "component_subtypes": ["exterior", "interior"],
            },
            "physical_properties": {
                "dimensions": {
                    "unit": "mm",
                    "length": 300,
                    "width": 200,
                    "height": 90,
                },
                "volume": {"value": 5400000, "unit": "mm³"},
                "area": {"value": 54000, "unit": "mm²"},
            },
            "applications": ["structural_walls", "foundation"],
        },
    )


class MaterialCostResponse(BaseModel):
    total_cost: float = Field(
        description="The total cost of the materials for the walls"
    )
    rationale: str = Field(
        description="A rationale for the total cost of the materials for the walls."
    )
    materials: list[str] = Field(
        description="The list of materials amount and cost used in the walls"
    )


def extract_walls_from_floor_plan():
    """Extract walls from a floor plan json."""
    floor_plans_dir = Path(__file__).resolve().parents[2] / "data" / "floor_plans"
    floor_plan_json = floor_plans_dir / "floor_plan_1.json"

    with open(floor_plan_json, "r") as f:
        floor_plan: defaultdict = json.load(f)

    layer_names: list[str] = [
        layer["properties"]["General"]["Layer"]
        for layer in floor_plan["data"]["collection"]
        if layer.get("properties")
        and layer["properties"].get("General")
        and layer["properties"]["General"].get("Layer")
    ]

    total_length = sum(
        float(layer["properties"]["Geometry"]["Length"].replace(" mm", ""))
        for layer in floor_plan["data"]["collection"]
        if layer.get("properties")
        and layer["properties"].get("Geometry")
        and layer["properties"]["Geometry"].get("Length")
    )
    total_length_in_meters = total_length / 1000
    logger.info("total_length_in_meters", total_length_in_meters=total_length_in_meters)
    total_area_in_m2 = total_length_in_meters * 2.5
    logger.info("total_area_in_m2", total_area_in_m2=total_area_in_m2)

    template = """You will be provided a list of layer names. Please read the list and extract the exact value that tells a wall is external, you must guess the type of the wall from the layer names.

    Example:
    Layer names:
    - WALLS - External wall
    - DOORS
    - WINDOWS
    - WALLS - Internal wall

    External wall name: WALLS - External wall
    
    Here's the list of layer names:
    {layer_names}
    """

    gpt = get_gpt()

    chain = langchain_prompt_from_text(template=template) | gpt.with_structured_output(
        ExternalWallName, method="json_schema"
    )

    resp = chain.invoke({"layer_names": "\n".join(layer_names)})
    logger.info("resp", resp=resp)

    external_wall_name = cast(ExternalWallName, resp)
    logger.info("external_wall_name", external_wall_name=external_wall_name.name)

    # Extract walls from floor plan
    walls: list[ExternalWall] = []
    for layer in floor_plan["data"]["collection"]:
        is_external_wall = (
            layer.get("properties")
            and layer["properties"].get("General")
            and layer["properties"]["General"].get("Layer") == external_wall_name.name
        )
        if is_external_wall and (
            layer.get("properties")
            and layer["properties"].get("Geometry")
            and layer["properties"]["Geometry"].get("Length")
            and layer["properties"]["Geometry"].get("Angle")
        ):
            # "Length": "4625.000 mm",
            # "Angle": "270.000 deg"
            length = float(layer["properties"]["Geometry"]["Length"].replace(" mm", ""))
            angle = float(layer["properties"]["Geometry"]["Angle"].replace(" deg", ""))
            walls.append(
                ExternalWall(
                    length=length,
                    angle=angle,
                )
            )

    # -

    logger.info("⛏️ Calculating material cost...")

    materials = [
        Material(
            name="Brick",
            description="Brick is a building material made from clay, fired in a kiln.",
            retail_price={"value": 0.35, "description": "0.35 USD per brick"},
            material_metadata={
                "properties": {
                    "component_types": ["wall"],
                    "component_subtypes": ["exterior", "interior"],
                },
                "physical_properties": {
                    "dimensions": {
                        "unit": "mm",
                        "length": 300,
                        "width": 200,
                        "height": 90,
                    },
                    "volume": {"value": 5400000, "unit": "mm³"},
                    "area": {"value": 27000, "unit": "mm²"},
                },
                "applications": ["structural_walls", "foundation"],
            },
        ),
        Material(
            name="Cement",
            description="Cement is a building material made from a mixture of clay, limestone, and gypsum, fired in a kiln.",
            retail_price={"value": 3, "description": "3 USD per 25kg bag"},
            material_metadata={
                "properties": {
                    "component_types": ["wall"],
                    "component_subtypes": ["exterior", "interior"],
                },
                "physical_properties": {
                    "weight": {"value": 25, "unit": "kg"},
                },
            },
        ),
        Material(
            name="Water",
            description="Water is a building material made from a mixture of clay, limestone, and gypsum, fired in a kiln.",
            retail_price={"value": 0, "description": "0 USD per m³"},
            material_metadata={
                "properties": {
                    "component_types": ["wall"],
                    "component_subtypes": ["exterior", "interior"],
                },
            },
        ),
        Material(
            name="Sand",
            description="Sand is a building material made from a mixture of clay, limestone, and gypsum, fired in a kiln.",
            retail_price={"value": 25, "description": "25 USD per m³"},
            material_metadata={
                "properties": {
                    "component_types": ["wall"],
                    "component_subtypes": ["exterior", "interior"],
                },
            },
        ),
    ]

    # -

    logger.info("💰 Calculating material cost...")

    template = """You are a constructor expert. You will be provided a list of materials and the total area of the walls. You must calculate the cost of the materials for the walls.

    To determine how many square meters of wall can be built using the provided mortar, we use the formula:

    A_wall = V_mortar / C_mortar

    Where:
    - `A_wall` = total wall area in square meters (m²)
    - `V_mortar` = available volume of mortar in cubic meters (m³)
    - `C_mortar` = mortar consumption per square meter of wall (m³/m²)

    To calculate the number of bricks required, we use:

    N_bricks = A_wall / A_brick

    Where:
    - `N_bricks` = total number of bricks needed
    - `A_brick` = area of a single brick in square meters (m²)

    ### Example Calculation:
    If:
    - `V_mortar = V_mortar m³`
    - `C_mortar = C_mortar m³/m²`
    - `A_brick = A_brick m²`

    Then:
    - `A_wall = V_mortar / C_mortar`
    - `N_bricks = A_wall / A_brick`
    
    Here's the list of materials:
    {materials}

    Here's the total area of the walls:
    {total_area_in_m2}

    The height of the wall is 3 meters.

    Return the total cost of the materials for the walls and a rationale for the total cost.
    """

    gpt = get_gpt()

    chain = langchain_prompt_from_text(template=template) | gpt.with_structured_output(
        MaterialCostResponse, method="json_schema"
    )
    resp = chain.invoke(
        {
            "materials": "\n\n".join(
                [material.model_dump_json() for material in materials]
            ),
            "total_area_in_m2": total_area_in_m2,
        }
    )
    logger.info("resp", resp=resp)
