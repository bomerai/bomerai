import json
import os
from typing import cast

import structlog
from pydantic import BaseModel
from draft_building_designs.prompts.pt.prompt import Sapatacdq
from draft_building_designs.models import DesignDrawingComponentMetadata
from draft_building_designs.prompts.utils import LanguageModelFactory
from ai.services.runnables import get_langfuse_callback_handler

logger = structlog.get_logger(__name__)


class Footingbom(BaseModel):
    uuid: str
    concrete_volume_in_cubic_meters: float
    steel_weight_in_kilograms: float
    justification: str
    rationale: str


class Footingboms(BaseModel):
    footingboms: list[Footingbom]


class Footing(BaseModel):
    uuid: str
    width: float | None = None
    length: float | None = None
    height: float | None = None
    bottom_reinforcement_x: str | None = None
    bottom_reinforcement_y: str | None = None
    top_reinforcement_x: str | None = None
    top_reinforcement_y: str | None = None
    references: str | None = None


def get_footing_from_design_drawing_component_metadata(
    design_drawing_component_metadata: DesignDrawingComponentMetadata,
) -> Footing:
    """Get a footing from a design drawing component metadata"""
    return Footing(
        uuid=str(design_drawing_component_metadata.uuid),
        width=design_drawing_component_metadata.data.get("width"),
        length=design_drawing_component_metadata.data.get("length"),
        height=design_drawing_component_metadata.data.get("height"),
        bottom_reinforcement_x=design_drawing_component_metadata.data.get(
            "bottom_reinforcement_x"
        ),
        bottom_reinforcement_y=design_drawing_component_metadata.data.get(
            "bottom_reinforcement_y"
        ),
        top_reinforcement_x=design_drawing_component_metadata.data.get(
            "top_reinforcement_x"
        ),
        top_reinforcement_y=design_drawing_component_metadata.data.get(
            "top_reinforcement_y"
        ),
    ).model_dump()


def calculate_bom_per_footing(
    *,
    design_drawing_component_metadata_uuid: str,
    language_code: str = "pt",
) -> Footingbom:
    from langchain_openai.chat_models import ChatOpenAI
    from ai.services.runnables import langchain_prompt_from_text

    """Generate a bill of materials for an external wall."""
    logger.info("Calculating bill of materials for footings")

    design_drawing_component_metadata = DesignDrawingComponentMetadata.objects.get(
        uuid=design_drawing_component_metadata_uuid
    )

    prompt_name = "calculate_bom_for_footing"
    # Get the language-specific model and prompt
    language_model_class, prompt_text = LanguageModelFactory.get_language_model(
        language_code, prompt_name
    )

    logger.info(f"Language model class: {language_model_class}")

    gpt = ChatOpenAI(
        model="grok-2-latest",
        openai_api_key=os.getenv("GROK_API_KEY"),
        openai_api_base="https://api.x.ai/v1",
        request_timeout=3000,
    )
    chain = langchain_prompt_from_text(
        prompt_text=prompt_text,
    ) | gpt.with_structured_output(language_model_class, method="json_schema")

    response = chain.invoke(
        {
            "context": get_footing_from_design_drawing_component_metadata(
                design_drawing_component_metadata=design_drawing_component_metadata
            ),
        },
        config={
            "callbacks": [get_langfuse_callback_handler()],
            "run_name": f"{prompt_name}_{language_code}",
        },
    )

    sapatacdq = cast(Sapatacdq, response)

    # TODO: add mapping to domain model
    footingbom = Footingbom(
        uuid=sapatacdq.uuid,
        concrete_volume_in_cubic_meters=sapatacdq.volume_de_betao_em_metros_cubicos,
        steel_weight_in_kilograms=sapatacdq.peso_da_armadura_em_quilogramas,
        justification=sapatacdq.justificacao,
        rationale=sapatacdq.raciocinio,
    )
    return footingbom
