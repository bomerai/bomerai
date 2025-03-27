import importlib
from typing import Type

import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)


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
            },
            "Sapatas": {
                "sapatas": "footings",
            },
            "Calculo": {
                "volume_de_betao_em_metros_cubicos": "concrete_volume_in_cubic_meters",
                "peso_da_armadura_em_quilogramas": "steel_weight_in_kilograms",
                "raciocinio": "rationale",
            },
            "Calculos": {
                "calculos": "boms",
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

        return target_model_class.model_validate(target_data)
