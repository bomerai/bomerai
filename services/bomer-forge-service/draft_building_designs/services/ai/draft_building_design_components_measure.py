import base64
import importlib
import os
from typing import Literal, Type, cast

import cv2
import pytesseract
import structlog
from PIL import Image
from pydantic import BaseModel
from django.conf import settings
from draft_building_designs.models import DraftBuildingDesignDrawingDocument

logger = structlog.get_logger(__name__)

TESSDATA_DIR = os.path.join(settings.BASE_DIR.parent, "tessdata")


# Base domain model for footings
class Footing(BaseModel):
    width: float | None
    length: float | None
    height: float | None
    bottom_reinforcement_x: str | None
    bottom_reinforcement_y: str | None
    top_reinforcement_x: str | None
    top_reinforcement_y: str | None
    justification: str | None
    references: str | None
    type: Literal["Sapata Isolada", "Sapata Corrida"] | None


class Footings(BaseModel):
    footings: list[Footing]


# Base domain model for columns
class Column(BaseModel):
    code: str
    width: float
    length: float
    height: float
    longitudinal_rebar: str
    stirrups: str
    type: str = "COLUMN"


class ColumnIPE(BaseModel):
    code: str | None = None
    description: str | None = None
    height: float | None = None
    type: str = "COLUMN_IPE"


class Columns(BaseModel):
    columns: list[Column]


class LanguageModelFactory:
    @staticmethod
    def get_language_model(
        language_code: str, prompt_name: str
    ) -> tuple[Type[BaseModel], str]:
        """
        Factory method to get the appropriate language model and prompt

        Args:
            language_code: The language code (e.g., 'pt_pt', 'en_us')
            model_name: The model name to load (e.g., 'footing')

        Returns:
            A tuple containing (ModelClass, prompt_text)
        """
        try:
            # Import the language-specific module
            module_path = f"draft_building_designs.prompts.{language_code}.prompt"
            language_module = importlib.import_module(module_path)

            # Get the model class and prompt
            prompt_text, model_name = getattr(
                language_module, f"get_{prompt_name}_prompt"
            )()
            model_class = getattr(language_module, model_name)

            return model_class, prompt_text
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load language model: {e}")
            raise ValueError(
                f"Unsupported language code or model: {language_code}, {model_name}"
            )


class ModelMapper:
    @staticmethod
    def map_to_domain(
        source_model: BaseModel, target_model_class: Type[BaseModel]
    ) -> BaseModel:
        """Maps a language-specific model to the domain model"""
        # This is a simple implementation. For complex mappings, consider a more robust approach
        mapping_registry = {
            # Map from Sapata (pt_pt) to Footing
            "Sapata": {
                "largura": "width",
                "comprimento": "length",
                "altura": "height",
                "armadura_inferior_x": "bottom_reinforcement_x",
                "armadura_inferior_y": "bottom_reinforcement_y",
                "armadura_superior_x": "top_reinforcement_x",
                "armadura_superior_y": "top_reinforcement_y",
                "justificacao": "justification",
                "referencias": "references",
                "tipo": "type",
            },
            "Sapatas": {
                "sapatas": "footings",
            },
            "Pilar": {
                "codigo": "code",
                "largura": "width",
                "comprimento": "length",
                "altura": "height",
                "armadura_longitudinal": "longitudinal_rebar",
                "estribos": "stirrups",
            },
            "Pilares": {
                "pilares": "columns",
            },
            # Add more mappings for other languages here
        }

        source_class_name = source_model.__class__.__name__
        if source_class_name not in mapping_registry:
            raise ValueError(f"No mapping defined for {source_class_name}")

        field_mapping = mapping_registry[source_class_name]
        target_data = {}

        for source_field, target_field in field_mapping.items():
            if hasattr(source_model, source_field):
                source_value = getattr(source_model, source_field)

                # Handle list of models (like list of Pilar -> list of Column)
                if isinstance(source_value, list) and all(
                    isinstance(item, BaseModel) for item in source_value
                ):
                    # Determine the target item class based on naming convention
                    # For example, if target_model_class is Columns, the items should be Column
                    target_item_class = globals().get(
                        target_field.rstrip("s").capitalize()
                    )
                    if target_item_class:
                        target_data[target_field] = [
                            ModelMapper.map_to_domain(item, target_item_class)
                            for item in source_value
                        ]
                    else:
                        # Fallback if we can't determine the target item class
                        target_data[target_field] = source_value
                else:
                    target_data[target_field] = source_value

        logger.info(f"Target data: {target_data}")
        return target_model_class.model_validate(target_data)


# -


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


def extract_footings_from_image(
    drawing_document_uuid: str, language_code: str = "pt"
) -> list[Footing]:
    """
    Extract footing metadata from a drawing document

    Args:
        drawing_document_uuid: The UUID of the drawing document
        language_code: The language code to use (default: pt)

    Returns:
        A Footing domain model with the extracted metadata
    """
    import json

    from langfuse.openai import OpenAI

    prompt_name = "extract_footings_from_design_drawing_document"
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
    return cast(Footings, domain_model).footings


def extract_column_from_image(
    *,
    drawing_document_uuid: str,
    language_code: str = "pt",
) -> Column:
    """
    Extract columns metadata from a drawing document

    Args:
        drawing_document_uuid: The UUID of the drawing document
        language_code: The language code to use (default: pt)

    Returns:
        A list of Column domain models with the extracted metadata
    """
    import json

    from langfuse.openai import OpenAI

    prompt_name = "extract_column_from_design_drawing_file"
    # Get the language-specific model and prompt
    language_model_class, prompt_text = LanguageModelFactory.get_language_model(
        language_code, prompt_name
    )

    # -

    drawing_document = DraftBuildingDesignDrawingDocument.objects.get(
        uuid=drawing_document_uuid
    )

    image_base64 = encode_image(drawing_document.file.path)

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
                            schema=language_model_class.model_json_schema(),
                        )}
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

    domain_model = ModelMapper.map_to_domain(language_specific_model, Column)
    return cast(Column, domain_model)
