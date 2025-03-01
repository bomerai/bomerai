from typing import Any, cast

import structlog
from pydantic import BaseModel, Field

from ai.services.runnables import (
    get_gpt,
    get_langfuse_callback_handler,
    langchain_prompt_from_langfuse,
)
from core.base_model import UnitOfMeasure
from draft_building_designs.models import DraftBuildingDesign
from building_components.models import (
    BuildingComponent,
    BuildingComponentType,
    BuildingComponentSubtype,
)
from materials.models import Material
from studies.models import Study

logger = structlog.get_logger(__name__)


class PotentialBuildingComponent(BaseModel):
    description: str
    area_in_square_meters: float


class RawMaterial(BaseModel):
    name: str
    dimensions: dict[str, Any] | None = None
    pieces_per_square_meter: float | None = None
    weight: str | None = None
    instructions: str | None = None


class Dimensions(BaseModel):
    length: float
    width: float
    height: float


class PickedMaterial(BaseModel):
    name: str = Field(..., description="The name of the material needed")
    quantity: float = Field(
        ...,
        description="The quantity of the material needed. The unit of measure is the same as the unit of measure of the material.",
    )
    unit_of_measure: str = Field(
        ...,
        description="An enum of the unit of measure. Here are the possible values: SQUARE_METERS, CUBIC_METERS, LITERS, KILOGRAMS.",
    )
    length: float | None = Field(
        None, description="The length of the material needed in CENTIMETERS."
    )
    width: float | None = Field(
        None, description="The width of the material needed in CENTIMETERS."
    )
    height: float | None = Field(
        None, description="The height of the material needed in CENTIMETERS."
    )
    justification: str | None = Field(
        None,
        description="The justification for the quantity of the material needed. This is a short explanation of why the quantity of the material is needed.",
    )


class PickedMaterials(BaseModel):
    picked_materials: list[PickedMaterial] = Field(
        ...,
        description="A list of materials with the quantity of each material needed to build the building component.",
    )


def generate_building_design_components(draft_building_design_uuid: str):
    """Generate a building design from a"""
    logger.info(
        f"Generating building components for draft building design uuid {draft_building_design_uuid}",
    )
    draft_building_design = DraftBuildingDesign.objects.get(
        uuid=draft_building_design_uuid
    )

    external_wall = BuildingComponent.objects.create_exterior_wall_component(
        draft_building_design=draft_building_design,
        description="External wall of the building of a house",
        dimensions={
            "length": 100,
            "height": 3,
            "unit": UnitOfMeasure.METERS,
        },
        type=BuildingComponentType.WALL,
        subtype=BuildingComponentSubtype.EXTERIOR,
    )

    similar_studies = Study.objects.get_similar_studies_for_draft_building_design(
        draft_building_design=draft_building_design,
    )
    logger.info(f"Found {len(similar_studies)} similar studies")

    # Create and generate the external wall
    candidate_materials = get_candidate_materials(
        similar_studies=similar_studies,
    )
    logger.info(f"Found {len(candidate_materials)} candidate materials")

    new_materials: dict[
        tuple[BuildingComponentType, BuildingComponentSubtype], list[Material]
    ] = {}
    picked_materials = calculate_external_wall_bom(
        building_component=external_wall,
        candidate_materials=candidate_materials[
            (BuildingComponentType.WALL, BuildingComponentSubtype.EXTERIOR)
        ],
    )
    logger.info(
        f"Picked {len(picked_materials)} materials for building component {external_wall.uuid} {external_wall.subtype} {external_wall.type}"
    )
    for picked_material in picked_materials:
        material, _ = Material.objects.get_or_create(
            name=picked_material.name,
            dimensions=Dimensions(
                length=picked_material.length,
                width=picked_material.width,
                height=picked_material.height,
            ),
        )
        new_materials[
            (BuildingComponentType.WALL, BuildingComponentSubtype.EXTERIOR)
        ].append(material)

    for (
        type_subtype,
        materials,
    ) in new_materials.items():
        logger.info(
            f"Linking {len(materials)} materials to building component {external_wall.uuid} {str(type_subtype)}"
        )
        for material in materials:
            BuildingComponent.objects.link_material_to_building_component(
                building_component_uuid=external_wall.uuid,
                material_uuid=material.uuid,
                quantity=picked_material.quantity,
                unit=picked_material.unit_of_measure,
                justification=picked_material.justification,
            )


def calculate_external_wall_bom(
    building_component: BuildingComponent,
    candidate_materials: list[Material],
) -> list[PickedMaterial]:
    """Generate a bill of materials for an external wall."""
    logger.info(
        f"Calculating bill of materials for external wall building component: {str(building_component.uuid)}"
    )

    # TODO: create a scraper to get additional materials from the internet
    additional_materials: list[RawMaterial] = []

    gpt = get_gpt()
    chain = langchain_prompt_from_langfuse(
        prompt_name="generate_bom_for_an_external_wall",
    ) | gpt.with_structured_output(PickedMaterials, method="json_schema")

    area_in_square_meters, _ = building_component.get_area()
    response = chain.invoke(
        {
            "candidate_materials": "\n".join(
                [
                    *[
                        RawMaterial(
                            name=material.name,
                            dimensions=Dimensions(
                                length=material.dimensions.get("length", 0),
                                width=material.dimensions.get("width", 0),
                                height=material.dimensions.get("height", 0),
                            ),
                            instructions=material.metadata.get("instructions"),
                            pieces_per_square_meter=material.metadata.get(
                                "pieces_per_square_meter"
                            ),
                            weight=material.metadata.get("weight"),
                        ).model_dump_json()
                        for material in candidate_materials
                    ],
                    *additional_materials,
                ]
            ),
            "external_wall_area_in_square_meters": area_in_square_meters,
        },
        config={
            "callbacks": [get_langfuse_callback_handler()],
            "run_name": "generate_bom_for_an_external_wall",
        },
    )

    return cast(list[PickedMaterial], response.picked_materials)


def calculate_internal_floor_bom():
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


def get_candidate_materials(
    *,
    similar_studies: list[Study],
) -> dict[tuple[BuildingComponentType, BuildingComponentSubtype], list[Material]]:
    """Pick common materials for a building component."""

    candidate_materials = {}

    building_components = BuildingComponent.objects.filter(
        source_studies__in=similar_studies,
    ).distinct()

    for building_component in building_components:
        candidate_materials = building_component.materials.all()
        building_component_type = building_component.type
        building_component_subtype = building_component.subtype
        candidate_materials[(building_component_type, building_component_subtype)] = (
            candidate_materials
        )

    return candidate_materials
