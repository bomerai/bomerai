from rest_framework.response import Response
from rest_framework.views import APIView
from celery.result import AsyncResult
from .serializers import CeleryTaskResultSerializer
from django_celery_results.models import TaskResult


class CeleryTaskResultView(APIView):
    def get(self, request, task_id):
        state = AsyncResult(task_id).state
        task = (
            TaskResult.objects.only("status", "result").filter(task_id=task_id).first()
        )

        return Response(
            CeleryTaskResultSerializer(
                {
                    "status": state,
                    "result": task.result,
                }
            ).data
        )
