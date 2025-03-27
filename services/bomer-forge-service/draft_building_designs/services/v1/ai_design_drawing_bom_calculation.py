import base64
import json
import os

import cv2
import structlog
from langfuse.openai import OpenAI
from pydantic import BaseModel, Field

from building_components.models import (
    BuildingComponentSubtype,
    BuildingComponentType,
)
from draft_building_designs.models import (
    DesignDrawing,
    DesignDrawingComponentMetadata,
    DesignDrawingComponentMetadataSubtype,
)
from draft_building_designs.prompts.utils import LanguageModelFactory

logger = structlog.get_logger(__name__)


class BuildingComponentMetadata(BaseModel):
    uuid: str
    component_data: dict
    subtype: str


class PickedBuildingComponent(BaseModel):
    component_metadata_uuid: str = Field(
        ...,
        description="O uuid do componente metadata escolhido",
    )
    code: str = Field(
        ...,
        description="O codigo do componente escolhido. Se ele for um pilar, considere o código escrito na imagem, exemplo P23. Jamais retorne mais de um código para o mesmo componente. Se não houver código, crie um novo.",
    )
    subtype: str = Field(
        ...,
        description="O subtipo do componente escolhido.",
    )


class PickedFootingComponent(BaseModel):
    component_metadata_uuid: str = Field(
        ...,
        description="O uuid do componente metadata escolhido",
    )
    code: str = Field(
        ...,
        description="A generated code for the footing component. Example: F1, F2, F3, etc.",
    )


class PickedColumnComponent(BaseModel):
    component_metadata_uuid: str = Field(
        ...,
        description="O uuid do componente metadata escolhido",
    )
    code: str = Field(
        ...,
        description="A generated code for the column component. Example: P1",
    )


class PickedBuildingComponentCluster(BaseModel):
    footing: PickedFootingComponent
    column: PickedColumnComponent


class PickedBuildingComponents(BaseModel):
    building_component_clusters: list[PickedBuildingComponentCluster]


def get_footings_metadata(footings: list[DesignDrawingComponentMetadata]):
    return "\n".join([json.dumps(footing.data) for footing in footings])


def get_columns_metadata(columns: list[DesignDrawingComponentMetadata]):
    return "\n".join([json.dumps(column.data) for column in columns])


def preprocess_image(image_path: str) -> str:
    """
    Pré-processa a imagem para melhorar a extração de texto via OCR.
    """
    # Carregar imagem em escala de cinza
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Aplicar filtro de desfoque para remover ruído
    img = cv2.GaussianBlur(img, (5, 5), 0)

    # Aplicar binarização (Otsu's Thresholding)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Salvar imagem processada temporariamente para depuração
    processed_path = image_path.replace(".png", "_processed.png")
    cv2.imwrite(processed_path, img)

    return processed_path  # Retorna o caminho da imagem processada


def encode_image(image_path):
    """Encodes an image in base64 for OpenAI API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_drawing_components_context(
    drawing_components: list[DesignDrawingComponentMetadata],
):
    return "\n".join(
        [
            BuildingComponentMetadata(
                uuid=str(drawing_component.uuid),
                component_data=drawing_component.data,
                subtype=drawing_component.subtype,
            ).model_dump_json()
            for drawing_component in drawing_components
        ]
    )


def generate_structural_design_evaluation(
    *, design_drawing_uuid: str, language_code: str = "pt"
):
    # TODO: Need to implement different strategies for different types of drawings and floors
    # TODO: Will need to figure out different prompts for different types of footings
    design_drawing = DesignDrawing.objects.get(uuid=design_drawing_uuid)
    building_design = design_drawing.building_design
    evaluation = building_design.evaluations.order_by("-created_at").first()

    footings = DesignDrawingComponentMetadata.objects.filter(
        design_drawing=design_drawing,
        subtype=DesignDrawingComponentMetadataSubtype.FOOTING,
    )

    columns = DesignDrawingComponentMetadata.objects.filter(
        design_drawing=design_drawing,
        subtype=DesignDrawingComponentMetadataSubtype.COLUMN,
    )

    drawing_components = list(footings) + list(columns)

    prompt_name = "building_design_building_components_extraction"
    _, prompt_text = LanguageModelFactory.get_language_model(language_code, prompt_name)

    # client = OpenAI(
    #     api_key=os.getenv("GROK_API_KEY"),
    #     base_url="https://api.x.ai/v1",
    #     timeout=3000,
    # )
    client = OpenAI()

    # processed_image_path = preprocess_image(evaluation.file.path)

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": PickedBuildingComponents.__name__,
                "schema": PickedBuildingComponents.model_json_schema(),
            },
        },
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text.format(
                            context=get_drawing_components_context(drawing_components),
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encode_image(evaluation.file.path)}",
                        },
                    },
                ],
            }
        ],
        name=f"{prompt_name}_{language_code}",
    )

    logger.info("Response", response=response.choices[0].message.content)
