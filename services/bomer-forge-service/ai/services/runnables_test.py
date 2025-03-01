from unittest import mock

import pytest
from asgiref.sync import async_to_sync

from ai.services.runnables import get_gpt, langchain_prompt_from_langfuse
from conftest import AiMocks


class MockLangchainPrompt:
    def get_langchain_prompt(self) -> str:
        """Simulate `get_langchain_prompt."""
        return "question {question}"


class MockLangfuse:
    """Fake Langfuse class."""

    def get_prompt(
        self, prompt_name: str, version: int | None = None
    ) -> MockLangchainPrompt:
        """Simulate `get_prompt."""
        return MockLangchainPrompt()


async def test_invokes_the_chain_callback_in_runnables(base_ai_mocks: AiMocks) -> None:
    with (
        mock.patch("ai.services.runnables.ChatOpenAI"),
        mock.patch("ai.services.runnables.langfuse", MockLangfuse()),
    ):
        chain = langchain_prompt_from_langfuse(prompt_name="test") | get_gpt()
        chain.invoke({})

        base_ai_mocks.chat_prompt_template_mock.from_template.assert_called_once_with(
            "question {question}"
        )


@pytest.mark.django_db()
@pytest.mark.skip_base_ai_mocks()
def test_does_not_init_langfuse_multiple_times() -> None:
    with mock.patch("ai.services.runnables.Langfuse") as langfuse_mock:
        langfuse_mock.return_value = MockLangfuse()
        langchain_prompt_from_langfuse(prompt_name="test")
        langchain_prompt_from_langfuse(prompt_name="test")

        langfuse_mock.assert_called_once()
