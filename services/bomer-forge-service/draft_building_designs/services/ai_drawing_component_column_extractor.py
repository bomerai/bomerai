import base64
import importlib
import os
from typing import Literal, Type, cast

import structlog
from django.conf import settings
from pydantic import BaseModel

from draft_building_designs.models import (
    DesignDrawingComponentMetadata,
    DesignDrawingComponentMetadataType,
    DesignDrawingComponentMetadataSubtype,
    DesignDrawingDocument,
)
from draft_building_designs.prompts.pt.prompt import Pilares, Pilar, PilarIPE

logger = structlog.get_logger(__name__)


class ColumnStirrupsDistribution(BaseModel):
    interval: str
    number: int
    spacing: float


class ColumnStarterRebarStirrupsDistribution(BaseModel):
    number: int


# Base domain model for columns
class Column(BaseModel):
    code: str
    width: float
    length: float
    height: float
    longitudinal_rebar: str
    longitudinal_rebar_stirrups_distribution: list[ColumnStirrupsDistribution]
    starter_rebar_height: float | None = None
    starter_rebar: str | None = None
    starter_rebar_stirrups_distribution: list[ColumnStarterRebarStirrupsDistribution]
    stirrup_diameter: str
    floors: list[str]
    type: str = "COLUMN"
    footing_uuid: str | None = None


class ColumnIPE(BaseModel):
    code: str | None = None
    description: str | None = None
    height: float | None = None
    floors: list[str] | None = None
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
            # Map from Pilar (pt_pt) to Column
            "Pilar": {
                "codigo": "code",
                "largura": "width",
                "comprimento": "length",
                "altura": "height",
                "armadura_longitudinal_diametro": "longitudinal_rebar_diameter",
                "armadura_longitudinal_estribos_numero": "longitudinal_rebar_stirrups_number",
                "armadura_longitudinal_estribos_espacamento": "longitudinal_rebar_stirrups_spacing",
                "arranque_altura": "starter_rebar_height",
                "arranque_diametro": "starter_rebar_diameter",
                "arranque_estribos_numero": "starter_rebar_stirrups_number",
                "estribo_diametro": "stirrup_diameter",
                "pisos": "floors",
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
) -> list[Column | ColumnIPE]:
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
    logger.info(
        f"Prompt: {prompt_text}, language_model_class: {language_model_class.model_json_schema()}"
    )

    # -

    drawing_document = DesignDrawingDocument.objects.get(uuid=drawing_document_uuid)

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
    language_specific_model: Pilares = language_model_class.model_validate(json_data)

    # Map to domain model
    # domain_model = ModelMapper.map_to_domain(language_specific_model, Columns)
    # return cast(Columns, domain_model).columns

    columns_grouped_by_code: list[Column | ColumnIPE] = []

    for column in language_specific_model.pilares:
        if isinstance(column, Pilar):
            longitudinal_rebar_stirrups_distribution = [
                ColumnStirrupsDistribution(
                    interval=stirrup.intervalo,
                    number=stirrup.numero,
                    spacing=stirrup.espacamento,
                )
                for stirrup in column.pilar_estribos
            ]
            starter_rebar_stirrups_distribution = [
                ColumnStarterRebarStirrupsDistribution(
                    number=stirrup.numero,
                )
                for stirrup in column.arranque_estribos
            ]
            columns_grouped_by_code.append(
                Column(
                    code=column.codigo,
                    width=column.largura,
                    length=column.comprimento,
                    height=column.altura,
                    longitudinal_rebar=column.armadura_longitudinal,
                    longitudinal_rebar_stirrups_distribution=longitudinal_rebar_stirrups_distribution,
                    starter_rebar=column.arranque,
                    starter_rebar_stirrups_distribution=starter_rebar_stirrups_distribution,
                    stirrup_diameter=column.estribo_diametro,
                    floors=column.pisos,
                )
            )

        elif isinstance(column, PilarIPE):
            columns_grouped_by_code.append(
                ColumnIPE(
                    code=column.codigo,
                    description=column.descricao,
                    height=column.altura,
                    floors=column.pisos,
                )
            )

    columns: list[Column | ColumnIPE] = []
    for column in columns_grouped_by_code:
        codes = column.code.split("=")
        for code in codes:
            if isinstance(column, Column):
                columns.append(
                    Column(
                        code=code,
                        **column.model_dump(exclude={"code"}),
                    )
                )
            elif isinstance(column, ColumnIPE):
                columns.append(
                    ColumnIPE(
                        code=code,
                        **column.model_dump(exclude={"code"}),
                    )
                )

    # extract starter rebar height from footings
    footings = DesignDrawingComponentMetadata.objects.filter(
        design_drawing=drawing_document.design_drawing,
        type=DesignDrawingComponentMetadataType.FOUNDATION_PLAN,
        subtype=DesignDrawingComponentMetadataSubtype.FOOTING,
    )

    for column in columns:
        for footing in footings:
            if isinstance(column, Column) and column.code in footing.data.get(
                "references", ""
            ):
                column.starter_rebar_height = footing.data.get("height")
                column.footing_uuid = str(footing.uuid)
    return columns
