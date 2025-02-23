from celery import shared_task

from draft_building_designs.services.ai_generate_building_design_from_prompt import (
    ai_generate_building_design_from_prompt as ai_generate_building_design_from_prompt_func,
)


@shared_task
def ai_generate_building_design_from_prompt(
    prompt: str,
    draft_building_design_uuid: str,
):
    ai_generate_building_design_from_prompt_func(prompt, draft_building_design_uuid)
