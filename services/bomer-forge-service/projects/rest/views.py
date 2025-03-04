from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from projects.models import Project
from projects.rest.serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Project model providing CRUD operations.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
