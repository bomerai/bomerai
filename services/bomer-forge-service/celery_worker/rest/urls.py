"""Celery Worker REST URLs"""

from django.urls import path
from .views import CeleryTaskResultView

urlpatterns = [
    path(
        "celery-task-result/<str:task_id>/",
        CeleryTaskResultView.as_view(),
        name="celery-task-result",
    ),
]
