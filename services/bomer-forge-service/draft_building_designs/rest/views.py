import io
import os
import tempfile

import structlog
from django.core.files.base import ContentFile
from pdf2image import convert_from_bytes
from PIL import Image
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from building_design_evaluations.models import BuildingDesignEvaluation
from draft_building_designs.models import (
    DesignDrawing,
    DesignDrawingComponentMetadata,
    DraftBuildingDesign,
)
from draft_building_designs.rest.serializers import (
    CreateDraftBuildingDesignSerializer,
    DesignDrawingComponentMetadataSerializer,
    DesignDrawingSerializer,
    DraftBuildingDesignEvaluationSerializer,
    DraftBuildingDesignSerializer,
    UploadDrawingDesignSerializer,
)
from draft_building_designs.services.ai_design_drawing_bom_calculation import (
    generate_structural_design_evaluation,
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
            design_drawing_component_metadata_type=serializer.validated_data[
                "design_drawing_component_metadata_type"
            ],
            design_drawing_component_metadata_subtype=serializer.validated_data[
                "design_drawing_component_metadata_subtype"
            ],
            strip_footing_length=serializer.validated_data.get("strip_footing_length"),
            is_strip_footing=serializer.validated_data.get("is_strip_footing", False),
        )
        return Response(
            DraftBuildingDesignSerializer(building_design).data,
            status=status.HTTP_201_CREATED,
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

    @action(detail=True, methods=["get"], url_path="design-drawings/summary")
    def get_design_drawings_summary(self, request, *args, **kwargs):
        building_design = DraftBuildingDesign.objects.get(uuid=str(kwargs["pk"]))
        return Response(
            DesignDrawingSerializer(building_design).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="evaluation")
    def run_evaluation(self, request, *args, **kwargs):
        serializer = DraftBuildingDesignEvaluationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        building_design = DraftBuildingDesign.objects.get(
            uuid=str(serializer.validated_data["building_design_uuid"])
        )

        file = serializer.validated_data["files"][0]

        BuildingDesignEvaluation.objects.create(
            draft_building_design=building_design,
            file=file,  # Use the potentially converted file
        )
        design_drawing = DesignDrawing.objects.filter(
            building_design=building_design,
            type=serializer.validated_data["design_drawing_type"],
        ).first()
        generate_structural_design_evaluation(
            design_drawing_uuid=str(design_drawing.uuid),
        )
        return Response(
            {"message": "Evaluation run successfully"},
            status=status.HTTP_200_OK,
        )


class DesignDrawingComponentMetadataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DesignDrawingComponentMetadata model providing CRUD operations.
    """

    queryset = DesignDrawingComponentMetadata.objects.all()
    serializer_class = DesignDrawingComponentMetadataSerializer
    permission_classes = [IsAuthenticated]
