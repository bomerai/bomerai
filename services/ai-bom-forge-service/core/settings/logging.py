"""Logging configuration."""

from typing import Any

from core.types.environment import env

__all__ = ("LOGGING",)

LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": True,
}

if env.bool("LOG_DB_QUERIES", False):
    DEBUG_LOGGING = {
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django.db.backends": {
                "level": "DEBUG",
            },
        },
        "root": {
            "handlers": ["console"],
        },
    }
    LOGGING = {**LOGGING, **DEBUG_LOGGING}
