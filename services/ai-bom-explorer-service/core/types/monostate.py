"""Monostate pattern impl."""

from typing import Any

__all__ = ("Monostate",)


class Monostate:
    """A monostate is a "conceptual singleton".

    All data members of a monostate are static, so all instances of the
    monostate use the same (static) data.

    NB. This class cannot be used directly.
    """

    __instance_state__: dict[str, Any]

    def __init_subclass__(cls) -> None:
        """Initialize subclass with a new shared dict."""
        cls.__instance_state__ = {}

    def __init__(self) -> None:
        """Initialize instance."""
        self.__dict__ = self.__class__.__instance_state__
