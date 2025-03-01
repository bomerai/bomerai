from __future__ import annotations

import os  # - Force import for mock
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any
from unittest import mock

import pytest
from django.core.cache import cache


@dataclass
class AiMocks:
    """Class for AI Mocks."""

    chat_open_ai_mock: mock.Mock
    langfuse_mock: mock.Mock
    chat_prompt_template_mock: mock.Mock


@pytest.fixture(autouse=True)
def clear_cache() -> None:
    """Clear the Django cache before test runs."""
    cache.clear()


@pytest.fixture(autouse=True)
def base_ai_mocks(request: Any) -> Generator[AiMocks, None, None] | Generator:
    """Mock GPT/Langfuse so we don't accidentally call out to them in a test."""
    if "skip_base_ai_mocks" in request.keywords:
        yield None
        return
    with (
        mock.patch("ai.services.runnables.ChatOpenAI") as chat_open_ai_mock,
        mock.patch("ai.services.runnables.langfuse") as langfuse_mock,
        mock.patch(
            "ai.services.runnables.ChatPromptTemplate"
        ) as chat_prompt_template_mock,
    ):
        yield AiMocks(
            chat_open_ai_mock=chat_open_ai_mock,
            langfuse_mock=langfuse_mock,
            chat_prompt_template_mock=chat_prompt_template_mock,
        )
