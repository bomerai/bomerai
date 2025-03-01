"""protocol_research_service error classes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.types.environment import EnvironmentValueType

__all__ = (
    "EnvironmentValidationFailure",
    "MandatoryEnvironmentVariableMissing",
)


class EnvironmentValidationFailure(EnvironmentError):
    """Environment value failed validation check."""

    def __init__(self, value: EnvironmentValueType) -> None:
        """Initialize instance."""
        super().__init__(f"Invalid environment variable value {value!r}")


class MandatoryEnvironmentVariableMissing(EnvironmentError):
    """Failure to read a required environment variable."""

    def __init__(self, name: str) -> None:
        """Initialize instance."""
        super().__init__(f"Mandatory environment variable {name!r} is missing")
