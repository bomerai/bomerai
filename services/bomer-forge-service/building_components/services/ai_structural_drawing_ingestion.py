import base64
from typing import List, Optional

import structlog
from pydantic import BaseModel, Field


logger = structlog.get_logger(__name__)


def encode_image(image_path):
    """Encodes an image in base64 for OpenAI API"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class StirrupDistribution(BaseModel):
    interval: str = Field(..., description="The interval range in cm")
    number: int = Field(..., description="Number of stirrups in this interval")
    spacing: Optional[str] = Field(..., description="Spacing between stirrups in cm")


class ColumnReinforcement(BaseModel):
    pillar_id: str = Field(..., description="The pillar identifier")
    pillar_perimeter: Optional[str] = Field(
        None,
        description="Perimeter of the pillar in cm. Example: 30x30cm",
    )
    longitudinal_rebar: Optional[str] = Field(
        None, description="Longitudinal reinforcement specification. Example: 4Ø12"
    )
    starter_rebar: Optional[str] = Field(
        None, description="Starter reinforcement specification. Example: 4Ø12"
    )
    starter_rebar_number: Optional[int] = Field(
        None, description="Number of starter reinforcement bars. Example: 4"
    )
    stirrup_diameter: Optional[str] = Field(
        None, description="Diameter of stirrups used. Example: Ø6"
    )
    stirrups_distribution: Optional[List[StirrupDistribution]] = Field(
        None, description="List of stirrup intervals and their spacing"
    )


class ColumnReinforcementList(BaseModel):
    columns: List[ColumnReinforcement]


def ingest_pillars_with_openai(*, file_path: str):
    """Ingest pillars with OpenAI"""
    from langfuse.openai import OpenAI
    import json

    client = OpenAI()
    image_base64 = encode_image(f"{file_path}")
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You are a precise data extraction assistant. Your task is to extract structured pillar reinforcement data from an image uploaded by the user. Provide the JSON file that represents the data in the image. Use this JSON schema: {ColumnReinforcementList.model_json_schema()}",
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
        name="ingest_pillars_data_with_openai",
    )

    json_data = json.loads(response.choices[0].message.content)
    return json_data
