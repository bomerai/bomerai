import structlog

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from draft_building_designs.models import DraftBuildingDesign
from draft_building_designs.rest.serializers import (
    CreateDraftBuildingDesignSerializer,
    DraftBuildingDesignSerializer,
)
from projects.models import Project

logger = structlog.get_logger(__name__)


class DraftBuildingDesignViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DraftBuildingDesign model providing CRUD operations.
    """

    queryset = DraftBuildingDesign.objects.all()
    serializer_class = DraftBuildingDesignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset for the DraftBuildingDesignViewSet.
        """
        from projects.models import Project

        project_uuid = self.request.query_params.get("project_uuid")
        project = Project.objects.get(uuid=project_uuid)

        return self.queryset.filter(project=project)

    def create(self, request, *args, **kwargs):
        serializer = CreateDraftBuildingDesignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.get(uuid=serializer.validated_data["project_uuid"])
        draft_building_design = (
            DraftBuildingDesign.objects.create_draft_building_design(
                project_uuid=str(project.uuid),
            )
        )

        return Response(
            DraftBuildingDesignSerializer(draft_building_design).data,
            status=status.HTTP_201_CREATED,
        )
