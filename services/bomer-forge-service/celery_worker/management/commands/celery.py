"""Definition for `python manage.py celery`."""

import shlex
import subprocess
from typing import Any

import structlog
from django.core.management.base import BaseCommand
from django.utils import autoreload

from celery_worker.celery import QueuesNames

logger = structlog.getLogger(__name__)


def restart_celery(*, queues: list[str] | None = None) -> None:
    """Restart celery."""
    cmd = 'pkill -f "celery worker"'
    # ruff: noqa: S603
    subprocess.run(shlex.split(cmd))
    subscribe_queues = ",".join(queues) if queues else "celery"
    cmd = f"celery -A celery_worker.celery worker --loglevel=info --pool threads --queues={subscribe_queues}"
    # ruff: noqa: S603
    subprocess.run(shlex.split(cmd))


class Command(BaseCommand):
    """Run celery in a way such that it auto restarts on code changing."""

    help = __doc__

    def handle(self, *_: Any, **__: Any) -> None:
        """Start celery in a way such that it auto restarts on code changing."""
        logger.info("Starting celery worker with autoreload...")

        autoreload.run_with_reloader(
            restart_celery, queues=[QueuesNames.DEFAULT, QueuesNames.FORGE_USER]
        )
