import json
import os
from tempfile import NamedTemporaryFile

import structlog
from ai.services.runnables import get_gpt, get_langfuse_callback_handler
from django.core.management.base import BaseCommand
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from draft_building_designs.models import DXFEntity

logger = structlog.get_logger(__name__)

ASSISTANT_ID = "asst_FQaQDG1GGSNy4BIqmo5zQQn1"


class Column(BaseModel):
    code: str = Field(
        ...,
        description="The code of the column. Example: P23",
    )
    width: float = Field(
        ...,
        description="The width of the column in centimeters. Example: 30",
    )
    length: float = Field(
        ...,
        description="The length of the column in centimeters. Example: 30",
    )
    height: float = Field(
        ...,
        description="The height of the column in centimeters. Example: 375",
    )


class Columns(BaseModel):
    columns: list[Column]


def upload_files():
    from openai import OpenAI

    json_files = []
    chunk_size = 500
    total_entities = DXFEntity.objects.count()
    for i in range(0, total_entities, chunk_size):
        chunk = DXFEntity.objects.all()[i : i + chunk_size]
        new_file = NamedTemporaryFile(
            suffix=".json",
            delete=False,
        )
        entities_json = []
        for entity in chunk:
            entities_json.append(entity.metadata)
        new_file.write(json.dumps(entities_json).encode("utf-8"))
        json_files.append(new_file.name)

    logger.info("⛏️ step 1: files created")

    client = OpenAI()
    gpt_files = []
    for json_file in json_files:
        gpt_files.append(
            client.files.create(
                file=open(json_file, "rb"),
                purpose="assistants",
            )
        )

    logger.info("⛏️ step 2: files uploaded to OpenAI")


class Command(BaseCommand):
    help = "Extract columns from the drawing design"

    def handle(self, *args, **kwargs):
        from ai.services.runnables import langchain_prompt_from_text

        content = []
        for document in DXFEntity.objects.exclude(
            metadata__type__in=["POLYLINE", "LINE"]
        ):
            content.append(document.metadata)

        gpt = ChatOpenAI(
            model="grok-2-latest",
            openai_api_key=os.getenv("GROK_API_KEY"),
            openai_api_base="https://api.x.ai/v1",
            request_timeout=10000,
        )
        # gpt = get_gpt()
        chain = (
            langchain_prompt_from_text(
                prompt_text="""
            You are a helpful assistant that extracts columns from a drawing.
            The drawing is a DXF file.
            The columns are represented by a code, width, length and height.
            The code is a string that starts with "P" followed by a number.
            The height is the sum of the intervals between the top of the column and the bottom of the column.
            The width and length are the width and length of the column.

            {context}
            """
            )
            | gpt.with_structured_output(Columns, method="json_schema")
        )

        response = chain.invoke(
            {
                "context": json.dumps(content),
            },
            config={
                "callbacks": [get_langfuse_callback_handler()],
                "run_name": "grok_extract_columns",
            },
        )

        logger.info(f"Columns: {response}")
