from typing import Any, cast

import structlog
from pydantic import BaseModel, Field

from ai.services.runnables import (
    get_gpt,
    get_langfuse_callback_handler,
    langchain_prompt_from_langfuse,
)
from core.base_model import UnitOfMeasure

logger = structlog.get_logger(__name__)


class BuildingComponent(BaseModel):
    description: str
    area_in_square_meters: float


class RawMaterial(BaseModel):
    name: str
    dimensions: dict[str, Any] | None = None
    pieces_per_square_meter: float | None = None
    weight: str | None = None
    instructions: str | None = None


class PickedMaterial(BaseModel):
    name: str = Field(..., description="The name of the material needed")
    quantity: float = Field(..., description="The quantity of the material needed")
    unit_of_measure: str = Field(..., description="The unit of measure of the material")
    weight: str | None = Field(None, description="The weight of the material needed")
    justification: str | None = Field(
        None, description="The justification for the quantity of the material needed"
    )


class PickedMaterials(BaseModel):
    picked_materials: list[PickedMaterial] = Field(
        ...,
        description="A list of materials with the quantity of each material needed to build the building component.",
    )


def generate_building_design_components(draft_building_design_uuid: str):
    """Generate a building design from a"""
    logger.info(
        f"Generating building design components with uuid {draft_building_design_uuid}",
    )
    picked_materials = calculate_bom_for_an_external_wall()
    logger.info(f"External wall picked materials: {picked_materials}")
    picked_materials = calculate_bom_for_a_internal_floor_component()
    logger.info(f"Internal floor picked materials: {picked_materials}")


def calculate_bom_for_an_external_wall():
    """Generate a bill of materials for an external wall."""
    # draft_building_design = DraftBuildingDesign.objects.get(
    #     uuid=draft_building_design_uuid
    # )

    draft_building_design = (
        "DraftBuildingDesign(uuid=UUID('00000000-0000-0000-0000-000000000000'))"
    )

    logger.info(
        f"Generating building design components for draft building design: {draft_building_design}"
    )

    external_wall = BuildingComponent(
        description="External wall of the building of a house",
        area_in_square_meters=100,
    )

    available_materials = _mock_get_similar_materials_for_building_component()

    gpt = get_gpt()
    chain = langchain_prompt_from_langfuse(
        prompt_name="generate_bom_for_an_external_wall",
    ) | gpt.with_structured_output(PickedMaterials, method="json_schema")

    response = chain.invoke(
        {
            "available_materials": "\n".join(
                [material.model_dump_json() for material in available_materials]
            ),
            "external_wall_area_in_square_meters": external_wall.area_in_square_meters,
        },
        config={
            "callbacks": [get_langfuse_callback_handler()],
            "run_name": "generate_bom_for_an_external_wall",
        },
    )
    logger.info(f"Response: {response}")
    return cast(list[PickedMaterial], response.picked_materials)


def calculate_bom_for_a_internal_floor_component():
    """Generate a bill of materials for a floor."""
    # draft_building_design = DraftBuildingDesign.objects.get(
    #     uuid=draft_building_design_uuid
    # )

    floor = BuildingComponent(
        description="Internal floor of the building",
        area_in_square_meters=100,
    )

    available_materials = [
        RawMaterial(
            name="Pvc floor",
            dimensions={
                "length": 1220,
                "width": 180,
                "unit": UnitOfMeasure.MILLIMETERS,
            },
            pieces_per_square_meter=5,
            instructions="The floor is made of PVC tiles. The tiles are 1220mm x 180mm and they are connected to each other with a tongue and groove system. Requires a latex underlay to be installed before the floor is installed.",
        ),
        RawMaterial(
            name="LATEX Underlay for Laminate Flooring",
            dimensions={
                "length": 10,
                "width": 1,
                "unit": UnitOfMeasure.METERS,
            },
            pieces_per_square_meter=0.1,
            instructions="The latex underlay is 1.5mm thick and 10m long. It is used to install the PVC tiles.",
        ),
    ]

    gpt = get_gpt()
    chain = langchain_prompt_from_langfuse(
        prompt_name="calculate_bom_for_a_internal_floor_component",
    ) | gpt.with_structured_output(PickedMaterials, method="json_schema")

    response = chain.invoke(
        {
            "available_materials": "\n".join(
                [material.model_dump_json() for material in available_materials]
            ),
            "floor_area_in_square_meters": floor.area_in_square_meters,
        },
        config={
            "callbacks": [get_langfuse_callback_handler()],
            "run_name": "calculate_bom_for_a_internal_floor_component",
        },
    )
    logger.info(f"Response: {response}")
    return cast(list[PickedMaterial], response.picked_materials)


def _mock_get_similar_materials_for_building_component() -> list[RawMaterial]:
    return [
        RawMaterial(
            name="Ceramic block",
            dimensions={
                "length": 375,
                "width": 250,
                "height": 238,
                "unit": UnitOfMeasure.MILLIMETERS,
            },
            pieces_per_square_meter=10.5,
            weight="19.3 kg",
        ),
        RawMaterial(
            name="Sand",
        ),
        RawMaterial(
            name="Mortar",
        ),
        RawMaterial(
            name="Cement",
        ),
        RawMaterial(
            name="Steel",
        ),
    ]
