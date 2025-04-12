import structlog
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from building_components.models import BuildingComponent, BuildingComponentType
from draft_building_designs.models import (
    DraftBuildingDesign,
    DraftBuildingDesignBuildingComponent,
    DraftBuildingDesignDrawingDocument,
    DraftBuildingDesignCalculationModule,
)
from draft_building_designs.rest.serializers import (
    CreateDraftBuildingDesignSerializer,
    DraftBuildingDesignBuildingComponentSerializer,
    DraftBuildingDesignCalculationModuleSerializer,
    DraftBuildingDesignSerializer,
    UploadDesignDrawingSerializer,
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

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-design-drawing-details-file",
    )
    def upload_design_drawing_details_file(self, request, *args, **kwargs):
        """
        Handle image files that contain details of the building design.
        """
        from draft_building_designs.services.ai_building_component_extraction import (
            extract_columns_from_drawing_design_document,
            extract_footings_from_drawing_design_document,
        )

        serializer = UploadDesignDrawingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        draft_building_design = DraftBuildingDesign.objects.get(
            uuid=serializer.validated_data["draft_building_design_uuid"]
        )
        logger.info(
            "Uploading footing component design drawing",
            draft_building_design_uuid=draft_building_design.uuid,
            files=serializer.validated_data["files"],
        )

        documents = []
        for file in serializer.validated_data["files"]:
            draft_building_design_drawing_document = (
                DraftBuildingDesignDrawingDocument.objects.create(
                    draft_building_design=draft_building_design,
                    file=file,
                )
            )
            documents.append(draft_building_design_drawing_document)

        # TODO: refactor
        if serializer.validated_data["type"] == "FOOTING":
            # TODO: refactor
            if serializer.validated_data["is_strip_footing"]:
                component_building_type = BuildingComponentType.objects.filter(
                    name="Continuous"
                ).first()
            else:
                component_building_type = BuildingComponentType.objects.filter(
                    name="Isolated"
                ).first()
            if not component_building_type:
                raise ValidationError({"detail": "Building component type not found"})

            for document in documents:
                # ai generate footing components
                footings = extract_footings_from_drawing_design_document(
                    drawing_document_uuid=str(document.uuid),
                )
                logger.info(
                    "Extracted footings from drawing design document",
                    footings=footings,
                )
                # TODO: need to add the footing length if it's a strip footing
                footing_components = [
                    BuildingComponent(
                        type=component_building_type,
                        description="generated from drawing document",
                        component_data=footing.model_dump(),
                    )
                    for footing in footings
                ]
                BuildingComponent.objects.bulk_create(footing_components)

                # link footing components to draft building design
                for footing_component in footing_components:
                    DraftBuildingDesign.objects.link_building_component_to_building_design(
                        building_component_uuid=str(footing_component.uuid),
                        building_design_uuid=str(draft_building_design.uuid),
                        justification="generated from drawing document",
                    )

        # TODO: refactor this
        if serializer.validated_data["type"] == "COLUMN":
            component_building_type = BuildingComponentType.objects.filter(
                name="Column"
            ).first()
            if not component_building_type:
                raise ValidationError({"detail": "Building component type not found"})
            for document in documents:
                columns = extract_columns_from_drawing_design_document(
                    drawing_document_uuid=str(document.uuid),
                )
                logger.info(
                    "Extracted columns from drawing design document",
                    columns=columns,
                )
                column_components = [
                    BuildingComponent(
                        type=component_building_type,
                        description="generated from drawing document",
                        component_data=column.model_dump(),
                    )
                    for column in columns
                ]
                BuildingComponent.objects.bulk_create(column_components)

                # TODO: reuse the footing code above
                # link column components to draft building design
                for column_component in column_components:
                    DraftBuildingDesign.objects.link_building_component_to_building_design(
                        building_component_uuid=str(column_component.uuid),
                        building_design_uuid=str(draft_building_design.uuid),
                        justification="generated from drawing document",
                    )

        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-files",
    )
    def upload_files(self, request, *args, **kwargs):
        serializer = UploadDesignDrawingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        draft_building_design = DraftBuildingDesign.objects.get(
            uuid=serializer.validated_data["draft_building_design_uuid"]
        )
        for file in serializer.validated_data["files"]:
            DraftBuildingDesignDrawingDocument.objects.create(
                draft_building_design=draft_building_design,
                file=file,
                type=serializer.validated_data["type"],
            )

        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="building-components",
        serializer_class=DraftBuildingDesignBuildingComponentSerializer,
    )
    def building_components(self, request, *args, **kwargs):
        """
        Get all building components for a draft building design.
        Filter by component type using the 'type' query parameter.
        """
        draft_building_design = DraftBuildingDesign.objects.get(uuid=self.kwargs["pk"])

        # Get component type from query parameters
        component_type = request.query_params.get("type")

        # Base query
        query = DraftBuildingDesignBuildingComponent.objects.filter(
            draft_building_design=draft_building_design,
        ).select_related("building_component")

        # Apply type filter if provided
        if component_type:
            query = query.filter(building_component__type=component_type)

        serializer = DraftBuildingDesignBuildingComponentSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["get"],
        url_path="column-components",
        serializer_class=DraftBuildingDesignBuildingComponentSerializer,
    )
    def list_column_components(self, request, *args, **kwargs):
        """
        Get all column components for a draft building design.
        """
        draft_building_design = DraftBuildingDesign.objects.get(uuid=self.kwargs["pk"])

        column_draft_building_design_building_components = (
            DraftBuildingDesignBuildingComponent.objects.filter(
                draft_building_design=draft_building_design,
                building_component__type__name="Column",
            ).select_related("building_component")
        )

        serializer = DraftBuildingDesignBuildingComponentSerializer(
            column_draft_building_design_building_components, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: remove
    @action(
        detail=True,
        methods=["post"],
        url_path="measure-project",
    )
    def measure_project(self, request, *args, **kwargs):
        """
        Measure the project of a draft building design.
        """
        serializer = UploadDesignDrawingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        draft_building_design = DraftBuildingDesign.objects.get(uuid=self.kwargs["pk"])
        logger.info(
            "Uploading footing component design drawing",
            draft_building_design_uuid=draft_building_design.uuid,
            files=serializer.validated_data["files"],
        )

        documents = []
        for file in serializer.validated_data["files"]:
            draft_building_design_drawing_document = (
                DraftBuildingDesignDrawingDocument.objects.create(
                    draft_building_design=draft_building_design,
                    file=file,
                )
            )
            documents.append(draft_building_design_drawing_document)

        pass

    # TODO: remove
    @action(
        detail=True,
        methods=["get"],
        url_path="calculation-modules",
        serializer_class=DraftBuildingDesignCalculationModuleSerializer,
    )
    def list_calculation_modules(self, request, *args, **kwargs):
        """
        Get all calculation modules for a draft building design.
        """
        draft_building_design = DraftBuildingDesign.objects.get(uuid=self.kwargs["pk"])
        calculation_modules = DraftBuildingDesignCalculationModule.objects.filter(
            draft_building_design=draft_building_design
        )
        serializer = DraftBuildingDesignCalculationModuleSerializer(
            calculation_modules, many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
