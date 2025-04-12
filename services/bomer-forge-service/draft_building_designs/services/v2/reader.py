"""
This module is responsible for reading the details of the building designs.
"""

import base64
import os
from typing import Literal, cast

import cv2
import pytesseract
import structlog
from building_components.models import BuildingComponent
from django.conf import settings
from langfuse.openai import OpenAI
from PIL import Image
from pydantic import BaseModel

from draft_building_designs.models import DraftBuildingDesignDrawingDocument
from draft_building_designs.prompts.utils import LanguageModelFactory, ModelMapper
from building_components.models import BuildingComponentType

logger = structlog.get_logger(__name__)

TESSDATA_DIR = os.path.join(settings.BASE_DIR.parent, "tessdata")


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


def extract_text_from_image(image_path: str, lang: str = "por") -> str:
    """
    Extrai texto da imagem usando Tesseract OCR.
    """
    processed_image = preprocess_image(image_path)

    # Executa OCR na imagem processada
    text = pytesseract.image_to_string(
        Image.open(processed_image),
        lang=lang,
        config=f"--tessdata-dir {TESSDATA_DIR}",
    )

    return text.strip()  # Remove espaços extras


def encode_image(image_path):
    """Encodes an image in base64 for OpenAI API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


DRAWING_TYPE = Literal["FOOTING", "COLUMN", "BEAM"]


def read_design_drawing_details_file(
    design_drawing_document: DraftBuildingDesignDrawingDocument,
    drawing_type: DRAWING_TYPE,
) -> None:
    """
    Read the details of the building design from the file.
    It may create components, beams, columns, etc.
    """
    match drawing_type:
        case "FOOTING":
            _extract_footings_from_drawing_design_document(
                drawing_document_uuid=design_drawing_document.uuid,
                language_code="pt",
            )
        case "COLUMN":
            pass
        case "BEAM":
            pass


# -


class Footing(BaseModel):
    """
    A footing is a concrete slab that supports a column or a wall.
    """

    width: float | None
    length: float | None
    height: float | None
    bottom_reinforcement_x: str | None
    bottom_reinforcement_y: str | None
    top_reinforcement_x: str | None
    top_reinforcement_y: str | None


class Footings(BaseModel):
    footings: list[Footing]


def _extract_footings_from_drawing_design_document(
    *, drawing_document_uuid: str, language_code: str = "pt"
) -> None:
    """
    Extract footing metadata from a drawing document

    Args:
        drawing_document_uuid: The UUID of the drawing document
        language_code: The language code to use (default: pt)

    Returns:
        A Footing domain model with the extracted metadata
    """
    import json

    prompt_name = "extract_footings_from_design_drawing_details_file"
    # Get the language-specific model and prompt
    language_model_class, prompt_text = LanguageModelFactory.get_language_model(
        language_code, prompt_name
    )

    # -

    drawing_document = DraftBuildingDesignDrawingDocument.objects.get(
        uuid=drawing_document_uuid
    )

    # Usa OCR para extrair texto antes de chamar GPT-4o
    extracted_text = extract_text_from_image(drawing_document.file.path)

    # TODO: make dynamic
    image_base64 = encode_image(
        f"{drawing_document.file.path.replace('.png', '_processed.png')}"
    )

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        {prompt_text.format(
                            schema=language_model_class.model_json_schema()
                        )}
                        
                        Texto extraído via OCR:
                        {extracted_text}
                        """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}",
                        },
                    },
                ],
            },
        ],
        name=f"{prompt_name}_{language_code}",
    )

    json_data = json.loads(response.choices[0].message.content)
    language_specific_model = language_model_class(**json_data)

    # Map to domain model
    domain_model = ModelMapper.map_to_domain(language_specific_model, Footings)
    footings = cast(Footings, domain_model).footings

    for footing in footings:
        BuildingComponent.objects.create(
            type=BuildingComponentType.FOOTING,
            component_data=footing.model_dump(),
        )
