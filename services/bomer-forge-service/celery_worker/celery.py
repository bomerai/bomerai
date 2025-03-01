"""Initialize Celery App for marking asynchronous tasks."""

import os
from enum import StrEnum
from typing import Any

import structlog
from celery import Celery
from celery.signals import setup_logging, task_failure, task_internal_error

# from ddtrace import config as ddtrace_config
# from ddtrace import patch
from django_structlog.celery.steps import DjangoStructLogInitStep

from core.logging import configure_logging

logger = structlog.getLogger(__name__)

# ddtrace_config.celery.service_name = os.environ.get("DD_SERVICE")
# patch(celery=True)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("celery_worker")

# A step to initialize django-structlog
app.steps["worker"].add(DjangoStructLogInitStep)


class QueuesNames(StrEnum):
    """Celery queues names."""

    FORGE_USER = "forge_user"
    DEFAULT = "celery"


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.result_backend = "django-db"
app.conf.cache_backend = "django-cache"
app.conf.result_extended = True
app.conf.task_track_started = True
app.conf.task_time_limit = 660  # 11 minutes
app.conf.task_soft_time_limit = 600  # 10 minutes

app.conf.task_routes = {
    "draft_building_designs.tasks.*": {"queue": QueuesNames.FORGE_USER},
}

# ruff: noqa: ERA001
# example:
# app.conf.beat_schedule = {
# "hello-world-every-ten-seconds": {
#     "task": "celery_worker.tasks.hello_world",
#     "schedule": 20.0,
#   },
# }

app.conf.beat_schedule = {}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@setup_logging.connect
def receiver_setup_logging(*_args: Any, **_kwargs: Any) -> None:
    """Configure logging for celery."""
    configure_logging()
    logger.info("Celery logging configured")


@task_failure.connect
@task_internal_error.connect
def handle_task_failure(
    *,
    task_id: str,
    exception: Exception,
    **kwargs: Any,
) -> None:
    """Handle task failure."""
    logger.exception(
        f"{type(exception).__name__}: {task_id} - {exception}",
        extra={"kwargs": kwargs},
    )
