"""Global log configuration.

Configures logging to:
 - Output on Lmabda correctly
 - Be in JSON format
 - Adds a few useful additional fields for analysis
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import structlog


if TYPE_CHECKING:
    from collections.abc import Sequence


__all__ = ("configure_logging",)


def configure_logging(
    log_level: str | None = None,
    log_format: str | None = None,
    pre_processors: Sequence | None = None,
    shared_processors: Sequence | None = None,
    additional_processors: Sequence | None = None,
) -> None:
    """Configure structlog."""
    log_level = log_level or "INFO"
    log_format = log_format or "plain"

    shared_processors = shared_processors or []
    shared_processors = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),  # stack_info = True
        structlog.processors.format_exc_info,  # exc_info = True
        *shared_processors,
    ]

    processors: list = []

    if pre_processors:
        processors.extend(pre_processors)

    processors.extend(
        [
            structlog.stdlib.filter_by_level,
            *shared_processors,
            # TraceInjector(),
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.CallsiteParameterAdder(
                parameters=(
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ),
            ),
        ],
    )

    if additional_processors:
        processors.extend(additional_processors)

    processors.append(structlog.stdlib.ProcessorFormatter.wrap_for_formatter)

    structlog.configure(
        context_class=dict,
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    renderer: structlog.dev.ConsoleRenderer | structlog.processors.JSONRenderer
    if log_format and log_format.lower() == "plain":
        renderer = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    handler = logging.StreamHandler()
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared_processors,  # type: ignore
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                renderer,
            ],
        ),
    )

    logging.captureWarnings(capture=True)

    logging.basicConfig(
        format="%(message)s",
        handlers=[handler],
        level=log_level.upper(),
        force=True,
    )
