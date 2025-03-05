import base64
import importlib
from typing import Type

import structlog
from pydantic import BaseModel
from draft_building_designs.models import DesignDrawingDocument

logger = structlog.get_logger(__name__)


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
                target_data[target_field] = getattr(source_model, source_field)

        logger.info(f"Target data: {target_data}")
        return target_model_class.model_validate(target_data)


def encode_image(image_path):
    """Encodes an image in base64 for OpenAI API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_footing_metadata(
    drawing_document_uuid: str, language_code: str = "pt"
) -> Footing:
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

    prompt_name = "extract_footing_metadata_from_design_drawing_document"
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
                            schema=language_model_class.model_json_schema()
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
    domain_model = ModelMapper.map_to_domain(language_specific_model, Footing)
    return domain_model
