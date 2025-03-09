from rest_framework.response import Response
from rest_framework.views import APIView
from celery_worker.celery import app
from .serializers import CeleryTaskResultSerializer
from django_celery_results.models import TaskResult
import structlog

logger = structlog.get_logger(__name__)


class CeleryTaskResultView(APIView):
    def get(self, request, task_id):
        state = app.AsyncResult(task_id).state

        task = (
            TaskResult.objects.only("status", "result").filter(task_id=task_id).first()
        )

        return Response(
            CeleryTaskResultSerializer(
                {
                    "status": state,
                    "result": task.result if task else None,
                }
            ).data
        )
