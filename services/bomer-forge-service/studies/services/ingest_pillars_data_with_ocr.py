import os
import json
from typing import List, Optional, cast

import structlog
from google.cloud import vision
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from ai.services.runnables import get_gpt, get_langfuse_callback_handler
import cv2
import numpy as np

logger = structlog.get_logger(__name__)


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
        None, description="Width and height of the column section in cm"
    )
    total_rebar_length: Optional[str] = Field(
        None, description="Total calculated reinforcement length"
    )


class ColumnReinforcementList(BaseModel):
    columns: List[ColumnReinforcement]


def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to grayscale if not already
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Denoise the image
    denoised = cv2.fastNlMeansDenoising(thresh)

    # Dilation to connect broken lines
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(denoised, kernel, iterations=1)

    return dilated


def extract_tables(preprocessed_img):
    # Find contours
    contours, _ = cv2.findContours(
        preprocessed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filter contours by area and shape
    tables = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Adjust threshold as needed
            x, y, w, h = cv2.boundingRect(cnt)
            if w / h > 0.5:  # Filter table-like shapes
                tables.append((x, y, w, h))

    return tables


def enhance_text(image):
    # Increase resolution
    scale_factor = 2
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    enlarged = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

    # Sharpen the image
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(enlarged, -1, kernel)

    return sharpened


def ingest_pillars_with_ocr():
    credentials_path = os.path.join(
        os.path.dirname(__file__), "bomer-ai-5903df29fa96.json"
    )
    client = vision.ImageAnnotatorClient.from_service_account_json(credentials_path)
    image_path = os.path.join(os.path.dirname(__file__), "pillars.png")

    # Preprocess the image
    preprocessed = preprocess_image(image_path)

    # Find and process tables
    tables = extract_tables(preprocessed)

    # Process each table region
    all_texts = []
    for x, y, w, h in tables:
        # Extract the table region
        table_region = preprocessed[y : y + h, x : x + w]

        # Enhance the text in the table
        enhanced = enhance_text(table_region)

        # Save the enhanced region to a temporary file
        temp_path = "temp_table.png"
        cv2.imwrite(temp_path, enhanced)

        # Process with Google Vision API
        with open(temp_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        image_context = vision.ImageContext(
            language_hints=["pt-BR"],
            text_detection_params=vision.TextDetectionParams(
                enable_text_detection_confidence_score=True
            ),
        )

        response = client.document_text_detection(
            image=image, image_context=image_context
        )

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(
                    response.error.message
                )
            )

        if response.text_annotations:
            all_texts.append(response.text_annotations[0].description)

        # Clean up temporary file
        os.remove(temp_path)

    # Combine all extracted text
    combined_text = "\n".join(all_texts)

    # Save extracted text for debugging
    with open(os.path.join(os.path.dirname(__file__), "pillars.txt"), "w") as f:
        f.write(combined_text)

    instructions = """
    You are a precise data extraction assistant. Your task is to extract structured pillar reinforcement data from the text below.
    Focus on identifying:
    - Pillar IDs
    - Longitudinal reinforcement specifications
    - Starter reinforcement details
    - Stirrup specifications and distributions
    - Column dimensions

    Text to analyze:
    {text}

    The data should be extracted in the following format:
    {format}
    """

    prompt = ChatPromptTemplate.from_template(instructions)

    gpt = get_gpt()
    chain = prompt | gpt.with_structured_output(ColumnReinforcementList)
    response = chain.invoke(
        {
            "text": combined_text,
            "format": json.dumps(ColumnReinforcementList.model_json_schema()),
        },
        config={
            "callbacks": [get_langfuse_callback_handler()],
            "run_name": "ingest_pillars_data",
        },
    )

    logger.info(
        "Ingested pillars data",
        result=cast(ColumnReinforcementList, response).model_dump(),
    )
