from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langfuse import Langfuse
from langfuse.callback import CallbackHandler as LangfuseCallbackHandler
import os

langfuse: Langfuse | None = None
langfuse_callback_handler: LangfuseCallbackHandler = None


# NOTE: This ensures a signle instance of Langfuse is used throughout the application
# But it does not ensure that the instance is refreshed with the latest values from the database.
# Restart the service if the langfuse keys are updated in the database.
def get_langfuse_instance() -> Langfuse:
    """Get a Langfuse instance."""
    global langfuse
    if langfuse is None:
        langfuse_kwargs = {
            "public_key": os.getenv("LANGFUSE_PUBLIC_KEY"),
            "secret_key": os.getenv("LANGFUSE_SECRET_KEY"),
            "host": os.getenv("LANGFUSE_HOST"),
        }
        langfuse = Langfuse(**langfuse_kwargs)

    return langfuse


def get_langfuse_callback_handler() -> LangfuseCallbackHandler:
    """Get a Langfuse callback handler."""
    global langfuse_callback_handler
    if langfuse_callback_handler is None:
        langfuse_callback_handler_kwargs = {
            "public_key": os.getenv("LANGFUSE_PUBLIC_KEY"),
            "secret_key": os.getenv("LANGFUSE_SECRET_KEY"),
            "host": os.getenv("LANGFUSE_HOST"),
        }
        langfuse_callback_handler = LangfuseCallbackHandler(
            **langfuse_callback_handler_kwargs
        )

    return langfuse_callback_handler


def get_gpt(*, model: str = "gpt-4o-2024-08-06") -> ChatOpenAI:
    """Initialize an instance of GPT with langfuse tracing."""
    return ChatOpenAI(model=model, temperature=0)


def langchain_prompt_from_langfuse(
    *, prompt_name: str, version: int | None = None
) -> ChatPromptTemplate:
    """Get a langchain prompt from text."""
    langfuse_prompt = get_langfuse_instance().get_prompt(prompt_name, version=version)
    template = ChatPromptTemplate.from_template(
        langfuse_prompt.get_langchain_prompt(),
    )
    template.metadata = {"langfuse_prompt": langfuse_prompt}
    return template
