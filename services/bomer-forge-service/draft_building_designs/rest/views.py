import structlog
from rest_framework import status, viewsets
from rest_framework.decorators import action
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

    def create(self, request, *args, **kwargs):
        serializer = CreateDraftBuildingDesignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.get(uuid=serializer.validated_data["project_uuid"])
        draft_building_design = (
            DraftBuildingDesign.objects.create_draft_building_design(
                project_uuid=str(project.uuid),
                name=serializer.validated_data["name"],
                description=serializer.validated_data["description"],
            )
        )

        return Response(
            DraftBuildingDesignSerializer(draft_building_design).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="upload-drawing-design")
    def upload_drawing_design(self, request, *args, **kwargs):
        pass
