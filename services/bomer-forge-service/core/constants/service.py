"""Global Formation Bio environment variables."""

from pathlib import Path

from urlpath import URL

from core.types.environment import env

__all__ = (
    "CELERY_BROKER_URL",
    "SERVICE_DATABASE_MIGRATION_URL",
    "SERVICE_DATABASE_URL",
    "SERVICE_HOST",
    "SERVICE_PORT",
    "SERVICE_SSL_CA_BUNDLE",
    "SERVICE_SSL_DIR",
    "SPARK_LOG_FORMAT",
    "SPARK_LOG_LEVEL",
)

## Spark Vars

SPARK_LOG_LEVEL = env.str(
    "SPARK_LOG_LEVEL",
    "INFO",
    validator=lambda level: level.upper()
    in (
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
        "NOTSET",
    ),
)
SPARK_LOG_FORMAT = env.str(
    "SPARK_LOG_FORMAT",
    "json",
    validator=lambda level: level.lower() in ("json", "plain"),
)

## Service Vars

SERVICE_HOST = env.str("SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = env.int("SERVICE_PORT", 3000)

SERVICE_DATABASE_URL = env.url(
    "SERVICE_DATABASE_URL",
    URL("postgresql://service_app_user:@localhost:5432/protocol_research_service"),
    validator=lambda url: url.scheme == "postgresql",
)

SERVICE_DATABASE_MIGRATION_URL = env.url(
    "SERVICE_DATABASE_URL",
    default=SERVICE_DATABASE_URL,
    validator=lambda url: url.scheme == "postgresql",
)

SERVICE_SSL_DIR = env.path("SERVICE_SSL_DIR", Path("/opt/bimini/ssl"))
SERVICE_SSL_CA_BUNDLE = env.path(
    "SERVICE_SSL_CA_BUNDLE", Path("/etc/ssl/certs/ca-certificates.crt")
)

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", "")
