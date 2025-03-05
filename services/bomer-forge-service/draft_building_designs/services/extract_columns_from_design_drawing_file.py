import base64
import importlib
from typing import Type

import structlog
from pydantic import BaseModel
from draft_building_designs.models import DesignDrawingDocument

logger = structlog.get_logger(__name__)


# Base domain model for columns
class Column(BaseModel):
    code: str | None
    width: float | None
    length: float | None
    height: float | None
    longitudinal_rebar_diameter: str | None
    longitudinal_rebar_stirrups_number: int | None
    longitudinal_rebar_stirrups_spacing: float | None
    starter_rebar_diameter: str | None
    starter_rebar_stirrups_number: int | None
    starter_rebar_stirrups_spacing: float | None
    stirrup_diameter: str | None
    justification: str | None
    level: int | None


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
        source_model: BaseModel, target_model_class: Type[BaseModel], many: bool = False
    ) -> BaseModel:
        """Maps a language-specific model to the domain model"""
        # This is a simple implementation. For complex mappings, consider a more robust approach
        mapping_registry = {
            # Map from Pilar (pt_pt) to Column
            "Pilar": {
                "codigo": "code",
                "largura": "width",
                "comprimento": "length",
                "altura": "height",
                "armadura_longitudinal_diametro": "longitudinal_rebar_diameter",
                "armadura_longitudinal_estribos_numero": "longitudinal_rebar_stirrups_number",
                "armadura_longitudinal_estribos_espacamento": "longitudinal_rebar_stirrups_spacing",
                "arranque_diametro": "starter_rebar_diameter",
                "arranque_estribos_numero": "starter_rebar_stirrups_number",
                "arranque_estribos_espacamento": "starter_rebar_stirrups_spacing",
                "estribo_diametro": "stirrup_diameter",
                "justificacao": "justification",
                "nivel": "level",
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


def encode_image(image_path):
    """Encodes an image in base64 for OpenAI API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_columns_metadata(
    drawing_document_uuid: str,
    language_code: str = "pt",
) -> list[Column]:
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

    prompt_name = "extract_columns_metadata_from_design_drawing_file"
    # Get the language-specific model and prompt
    language_model_class, prompt_text = LanguageModelFactory.get_language_model(
        language_code, prompt_name
    )
    logger.info(f"Prompt: {prompt_text}, language_model_class: {language_model_class}")

    # -

    drawing_document = DesignDrawingDocument.objects.get(uuid=drawing_document_uuid)
    client = OpenAI()
    image_base64 = encode_image(f"{drawing_document.file.path}")
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text.format(
                            schema=language_model_class.model_json_schema(),
                        ),
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
    domain_model = ModelMapper.map_to_domain(
        language_specific_model, Columns, many=True
    )
    return domain_model
