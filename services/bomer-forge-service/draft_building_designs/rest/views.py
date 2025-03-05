import structlog

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from draft_building_designs.models import (
    DesignDrawing,
    DraftBuildingDesign,
)
from draft_building_designs.rest.serializers import (
    CreateDraftBuildingDesignSerializer,
    DraftBuildingDesignSerializer,
    DesignDrawingSerializer,
    UploadDrawingDesignSerializer,
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

    @action(detail=True, methods=["post"], url_path="upload-drawing-design")
    def upload_drawing_design(self, request, *args, **kwargs):
        serializer = UploadDrawingDesignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        building_design = DraftBuildingDesign.objects.get(
            uuid=str(serializer.validated_data["building_design_uuid"])
        )

        DraftBuildingDesign.objects.upload_drawing_design(
            building_design_uuid=str(building_design.uuid),
            files=serializer.validated_data["files"],
            design_drawing_type=serializer.validated_data["design_drawing_type"],
            design_drawing_plan_type=serializer.validated_data[
                "design_drawing_plan_type"
            ],
            design_drawing_plan_subtype=serializer.validated_data[
                "design_drawing_plan_subtype"
            ],
        )
        return Response(
            DraftBuildingDesignSerializer(building_design).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="design-drawings")
    def get_design_drawings(self, request, *args, **kwargs):
        building_design = DraftBuildingDesign.objects.get(uuid=str(kwargs["pk"]))
        user = request.user
        if building_design.project.created_by != user:
            return Response(
                {"detail": "You do not have permission to access this resource"},
                status=status.HTTP_403_FORBIDDEN,
            )

        design_drawings = DesignDrawing.objects.filter(building_design=building_design)
        return Response(
            DesignDrawingSerializer(design_drawings, many=True).data,
            status=status.HTTP_200_OK,
        )
