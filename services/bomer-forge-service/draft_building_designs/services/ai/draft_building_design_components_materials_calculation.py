"""
This module contains the logic for calculating the materials for the draft building design.
"""

import structlog
from ai.services.runnables import (
    get_gpt,
    get_langfuse_callback_handler,
    langchain_prompt_from_langfuse,
)
from pydantic import BaseModel, Field

from draft_building_designs.models import DraftBuildingDesign
from building_components.models import BuildingComponent, BuildingComponentType

logger = structlog.get_logger(__name__)


class ComponentBillOfMaterials(BaseModel):
    """
    This class represents the bill of materials for a single building component.
    """

    steel_weight: float = Field(
        ...,
        description="The weight of the steel in the building component in kilograms.",
    )
    concrete_volume: float = Field(
        ...,
        description="The volume of the concrete in the building component in cubic meters.",
    )
    rationale: str = Field(
        ...,
        description="The rationale for the calculation of the bill of materials.",
    )


class ColumnComponentData(BaseModel):
    """
    This class represents the data for a column component.
    """

    height: str
    width: str
    length: str
    longitudinal_reinforcement: str
    transverse_reinforcement: str


class FootingComponentData(BaseModel):
    """
    This class represents the data for a footing component.
    """

    height: str
    width: str
    length: str
    reinforcement_bars: list[str]


class BeamComponentData(BaseModel):
    """
    This class represents the data for a beam component.
    """

    height: str
    width: str
    length: str
    longitudinal_reinforcement: str
    stirrups: list[str]


class SlabComponentData(BaseModel):
    """
    This class represents the data for a slab component.
    """

    area: str
    thickness: str


def _get_column_component_data(
    *, building_component: BuildingComponent
) -> ColumnComponentData:
    """
    This function gets the data for a column component.
    """
    return ColumnComponentData(
        height=f"{building_component.component_data.get('height')}cm",
        width=f"{building_component.component_data.get('width')}cm",
        length=f"{building_component.component_data.get('length')}cm",
        longitudinal_reinforcement=building_component.component_data.get(
            "longitudinal_rebar"
        ),
        transverse_reinforcement=building_component.component_data.get("stirrups"),
    )


def _get_footing_component_data(
    *, building_component: BuildingComponent
) -> FootingComponentData:
    """
    This function gets the data for a footing component.
    """
    reinforcement_bars = []
    reinforcements = [
        "top_reinforcement_x",
        "bottom_reinforcement_x",
        "top_reinforcement_y",
        "bottom_reinforcement_y",
    ]
    for reinforcement in reinforcements:
        if building_component.component_data.get(reinforcement):
            reinforcement_bars.append(
                building_component.component_data.get(reinforcement)
            )

    return FootingComponentData(
        height=f"{building_component.component_data.get('height')}cm",
        width=f"{building_component.component_data.get('width')}cm",
        length=f"{building_component.component_data.get('length')}cm",
        reinforcement_bars=reinforcement_bars,
    )


def _get_beam_component_data(
    *, building_component: BuildingComponent
) -> BeamComponentData:
    """
    This function gets the data for a beam component.
    """
    longitudinal_reinforcement = f"{building_component.component_data.get('longitudinal_reinforcement_quantity')}Ø{building_component.component_data.get('longitudinal_reinforcement_diameter')}"
    stirrups = [
        f"{building_component.component_data.get('stirrups_quantity')}Ø{building_component.component_data.get('stirrups_diameter')}"
    ]

    return BeamComponentData(
        height=f"{building_component.component_data.get('height')}cm",
        width=f"{building_component.component_data.get('width')}cm",
        length=f"{building_component.component_data.get('length')}cm",
        longitudinal_reinforcement=longitudinal_reinforcement,
        stirrups=stirrups,
    )


def _get_slab_component_data(
    *, building_component: BuildingComponent
) -> SlabComponentData:
    """
    This function gets the data for a slab component.
    """
    return SlabComponentData(
        area=f"{building_component.component_data.get('area')}m²",
        thickness=f"{building_component.component_data.get('thickness')}cm",
    )


def get_component_data(*, building_component: BuildingComponent) -> BaseModel:
    """
    This function gets the data for a building component.
    """
    match building_component.type:
        case BuildingComponentType.COLUMN:
            return _get_column_component_data(building_component=building_component)
        case BuildingComponentType.FOOTING:
            return _get_footing_component_data(building_component=building_component)
        case BuildingComponentType.BEAM:
            return _get_beam_component_data(building_component=building_component)
        case BuildingComponentType.SLAB:
            return _get_slab_component_data(building_component=building_component)
        case _:
            raise ValueError(
                f"Invalid building component type: {building_component.component_type}"
            )


def generate_draft_building_design_components_bom(
    *, draft_building_design_uuid: str
) -> ComponentBillOfMaterials:
    """
    This function generates the bill of materials for the footing.
    """
    gpt = get_gpt()

    draft_building_design = DraftBuildingDesign.objects.get(
        uuid=draft_building_design_uuid
    )

    building_components = draft_building_design.building_components.filter()

    for building_component in building_components:
        chain = langchain_prompt_from_langfuse(
            prompt_name="calculate_building_component_bom"
        ) | gpt.with_structured_output(ComponentBillOfMaterials, method="json_schema")

        bom = chain.invoke(
            {
                "context": get_component_data(
                    building_component=building_component
                ).model_dump_json()
            },
            config={
                "callbacks": [get_langfuse_callback_handler()],
                "run_name": "generate_draft_building_design_components_bom",
            },
        )

        building_component.component_data["bom"] = bom.model_dump()
        building_component.save()
