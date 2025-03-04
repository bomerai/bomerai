import structlog
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from building_components.rest.serializers import (
    UploadFoundationMetadataSerializer,
)
from draft_building_designs.models import DraftBuildingDesign

logger = structlog.get_logger(__name__)


@api_view(["GET"])
def building_component_list(request):
    logger.info("BuildingComponentList list request")
    return Response({"message": "Hello, world!"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ingest_foundation_metadata(request):
    logger.info("Ingesting foundation metadata")

    serializer = UploadFoundationMetadataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    building_design = DraftBuildingDesign.objects.get(
        uuid=serializer.validated_data["building_design_uuid"],
        project__created_by=request.user,
    )

    try:
        files = serializer.validated_data["files"]
        if not files:
            return Response({"error": "No files provided"}, status=400)

        return Response({"message": "Files uploaded successfully"})

    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}")
        return Response({"error": str(e)}, status=500)
