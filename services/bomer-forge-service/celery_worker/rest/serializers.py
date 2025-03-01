from rest_framework import serializers
from enum import StrEnum


class CeleryTaskStatus(StrEnum):
    """Celery task statuses.

    Docs here: https://docs.celeryq.dev/en/main/userguide/tasks.html#task-states
    """

    FAILURE = "FAILURE"
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    RETRY = "RETRY"
    REVOKED = "REVOKED"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"


class CeleryTaskResultSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=CeleryTaskStatus)
    result = serializers.JSONField()
