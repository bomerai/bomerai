"""ConfigurableVariables for this repo."""

import structlog
from pydantic import BaseModel

from configurable_variables.models import ConfigurableVariable

logger = structlog.getLogger(__name__)


class _Constants(BaseModel):
    """ConfigurableVariables for this repo."""

    OPENAI_API_KEY: str | None = None
    GOOGLE_AUTH_CLIENT_ID: str | None = None
    LANGFUSE_HOST: str = "https://us.cloud.langfuse.com"
    LANGFUSE_PUBLIC_KEY: str = "pk-lf-cd4b838a-179d-41f5-821b-6997d0af1ef8"
    LANGFUSE_SECRET_KEY: str | None = None
    FORGE_FRONTEND_URL: str = "https://localhost:3000"
    SEND_LANGFUSE_TRACES: bool = True


class _AppConstants:
    """Get all configurable variables from the database."""

    _values: _Constants | None = None

    async def values(self) -> _Constants:
        """Get the app constants from the database."""
        if self._values is None:
            await self.set_values()

        if not self._values:
            msg = "DB constants have not been set."
            raise ValueError(msg)

        return self._values

    async def set_values(self) -> None:
        """Set all configurable variables from the database."""
        self._values = _Constants(
            **{
                conf.name: conf.value
                async for conf in ConfigurableVariable.objects.all()
            }
        )


constants = _AppConstants()
