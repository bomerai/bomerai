import json
import os
from typing import cast

import structlog
from pydantic import BaseModel
from draft_building_designs.prompts.pt.prompt import Calculo
from draft_building_designs.models import DraftBuildingDesignBuildingComponent
from building_components.models import BuildingComponent
from draft_building_designs.prompts.utils import LanguageModelFactory
from ai.services.runnables import get_langfuse_callback_handler, get_gpt

logger = structlog.get_logger(__name__)


class Bom(BaseModel):
    concrete_volume_in_cubic_meters: float
    steel_weight_in_kilograms: float
    rationale: str


class Boms(BaseModel):
    boms: list[Bom]


def get_component_data(
    building_component: BuildingComponent,
) -> str:
    """Get a footing from a design drawing component metadata"""
    return json.dumps(building_component.component_data)


def generate_bill_of_materials_for_component(
    *,
    draft_building_design_building_component_uuid: str,
    language_code: str = "pt",
) -> Boms:
    from langchain_openai.chat_models import ChatOpenAI
    from ai.services.runnables import langchain_prompt_from_text

    """Generate a bill of materials for an external wall."""
    logger.info("Calculating bill of materials for footings")
    draft_building_design_building_component = (
        DraftBuildingDesignBuildingComponent.objects.select_related(
            "building_component"
        ).get(uuid=draft_building_design_building_component_uuid)
    )
    building_component = draft_building_design_building_component.building_component

    prompt_name = "generate_component_bom"
    # Get the language-specific model and prompt
    language_model_class, prompt_text = LanguageModelFactory.get_language_model(
        language_code, prompt_name
    )

    logger.info(f"Language model class: {language_model_class}")

    gpt = ChatOpenAI(
        model="grok-2-latest",
        openai_api_key=os.getenv("GROK_API_KEY"),
        openai_api_base="https://api.x.ai/v1",
        request_timeout=10000,
    )
    # gpt = get_gpt()
    chain = langchain_prompt_from_text(
        prompt_text=prompt_text,
    ) | gpt.with_structured_output(language_model_class, method="json_schema")

    response = chain.invoke(
        {
            "context": get_component_data(building_component=building_component),
        },
        config={
            "callbacks": [get_langfuse_callback_handler()],
            "run_name": f"{prompt_name}_{language_code}",
        },
    )

    calculo = cast(Calculo, response)

    # TODO: add mapping to domain model
    bom = Bom(
        concrete_volume_in_cubic_meters=calculo.volume_de_betao_em_metros_cubicos,
        steel_weight_in_kilograms=calculo.peso_da_armadura_em_quilogramas,
        rationale=calculo.raciocinio,
    )

    building_component.component_bom = bom.model_dump()
    building_component.save(update_fields=["component_bom"])
    logger.info(
        "Bill of materials generated for component",
        building_component_uuid=building_component.uuid,
    )
    return
