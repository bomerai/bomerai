import structlog
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from building_components.models import BuildingComponent
from building_components.rest.serializers import (
    BuildingComponentSerializer,
    CreateBuildingComponentSerializer,
)

logger = structlog.get_logger(__name__)


class BuildingComponentViewSet(ModelViewSet):
    queryset = BuildingComponent.objects.all()
    serializer_class = BuildingComponentSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        url_path="bulk-create",
    )
    def bulk_create(self, request, *args, **kwargs):
        """
        Create a new building component.
        """
        from draft_building_designs.models import DraftBuildingDesign

        serializer = CreateBuildingComponentSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        for component in serializer.validated_data:
            logger.info("Creating building component", component=component)
            draft_building_design = DraftBuildingDesign.objects.get(
                uuid=component["draft_building_design_id"]
            )

            building_component = BuildingComponent.objects.create(
                description="manually created",
                type=component["type"],
                component_data=component["component_data"],
            )

            DraftBuildingDesign.objects.link_building_component_to_building_design(
                building_design_uuid=str(draft_building_design.uuid),
                building_component_uuid=str(building_component.uuid),
            )

        return Response(
            {"message": "Building components created successfully"},
            status=status.HTTP_201_CREATED,
        )
