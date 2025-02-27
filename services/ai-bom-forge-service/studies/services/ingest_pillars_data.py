import base64
import os
from typing import List, Optional, cast

import structlog
from pydantic import BaseModel, Field

from ai.services.runnables import (
    get_gpt,
    get_langfuse_callback_handler,
)

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
    dimensions: Optional[dict] = Field(
        None,
        description="Width and height of the column section in cm. Example: {'width': '30 cm', 'height': '30 cm'}",
    )
    total_rebar_length: Optional[str] = Field(
        None, description="Total calculated reinforcement length"
    )


class ColumnReinforcementList(BaseModel):
    columns: List[ColumnReinforcement]


def ingest_pillars_data_with_langchain():
    from langchain.prompts import ChatPromptTemplate
    from openai import OpenAI

    image_path = os.path.join(os.path.dirname(__file__), "pillars.png")
    image_base64 = encode_image(image_path)
    # Initialize OpenAI client and upload image
    # client = OpenAI()
    # with open(image_path, "rb") as image_file:
    #     response = client.files.create(file=image_file, purpose="assistants")
    # image_file_id = response.id

    prompt = ChatPromptTemplate.from_template(
        """
        You are a precise data extraction assistant. Your task is to extract structured pillar reinforcement data from an image uploaded by the user.

        {image_url}

        - Ensure numbers are exactly as they appear.
        - Ensure that lists maintain the correct order of data as seen in the image.

        This is an example of how the extracted data should look like:
        {example}
        
        Don't add any other text or explanations.
        """
    )

    gpt = get_gpt()
    chain = prompt | gpt.with_structured_output(ColumnReinforcementList)
    result = chain.invoke(
        {
            "image_url": f"data:image/png;base64,{image_base64}",
            "example": ColumnReinforcementList(
                columns=[
                    ColumnReinforcement(
                        pillar_id="P1=P14=P15=P21",
                        longitudinal_rebar="4Ø12",
                        starter_rebar="4Ø12",
                        starter_rebar_number=4,
                        stirrup_diameter="Ø6",
                        stirrups_distribution=[
                            StirrupDistribution(
                                interval="100-400", number=3, spacing="100 cm"
                            ),
                            StirrupDistribution(
                                interval="400-800", number=4, spacing="200 cm"
                            ),
                        ],
                        dimensions={"width": "30 cm", "height": "30 cm"},
                        total_rebar_length="1000 cm",
                    )
                ]
            ).model_dump_json(),
        },
        config={
            "callbacks": [get_langfuse_callback_handler()],
            "run_name": "ingest_pillars_data",
        },
    )

    # client.files.delete(image_file_id)

    logger.info(
        "Ingested pillars data",
        result=cast(ColumnReinforcementList, result).model_dump(),
    )


def ingest_pillars_with_openai():
    from langfuse.openai import OpenAI
    import json

    client = OpenAI()
    image_path = os.path.join(os.path.dirname(__file__), "pillars.png")
    # with open(image_path, "rb") as image_file:
    #     response = client.files.create(file=image_file, purpose="assistants")
    # image_file_id = response.id
    image_base64 = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"provide the JSON file that represents the data in the image. Use this JSON schema: {ColumnReinforcementList.model_json_schema()}",
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
    logger.info("Ingested pillars data", result=json_data)
    filename_without_extension = os.path.splitext(image_path)[0]
    with open(
        f"{os.path.join(os.path.dirname(__file__), f'{filename_without_extension}.json')}",
        "w",
    ) as f:
        json.dump(json_data, f, indent=4)

    logger.info("Ingested pillars data", result=json_data)
