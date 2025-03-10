from rest_framework import serializers
from draft_building_designs.models import (
    DraftBuildingDesign,
    DesignDrawing,
    DesignDrawingType,
    DesignDrawingComponentMetadata,
    DesignDrawingComponentMetadataType,
    DesignDrawingComponentMetadataSubtype,
)


class DraftBuildingDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftBuildingDesign
        fields = "__all__"


class CreateDraftBuildingDesignSerializer(serializers.Serializer):
    project_uuid = serializers.UUIDField()


class UploadDrawingDesignSerializer(serializers.Serializer):
    building_design_uuid = serializers.UUIDField()
    files = serializers.ListField(child=serializers.FileField())
    design_drawing_type = serializers.ChoiceField(
        choices=DesignDrawingType.choices,
    )
    design_drawing_component_metadata_type = serializers.ChoiceField(
        choices=DesignDrawingComponentMetadataType.choices,
    )
    design_drawing_component_metadata_subtype = serializers.ChoiceField(
        choices=DesignDrawingComponentMetadataSubtype.choices,
    )
    strip_footing_length = serializers.IntegerField(required=False)
    is_strip_footing = serializers.BooleanField(required=False)


class DesignDrawingComponentMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignDrawingComponentMetadata
        fields = "__all__"


class DesignDrawingSerializer(serializers.ModelSerializer):
    design_drawing_components_metadata = DesignDrawingComponentMetadataSerializer(
        many=True
    )

    class Meta:
        model = DesignDrawing
        fields = "__all__"


class DraftBuildingDesignEvaluationSerializer(serializers.Serializer):
    building_design_uuid = serializers.UUIDField()
    files = serializers.ListField(child=serializers.FileField())
    design_drawing_type = serializers.ChoiceField(
        choices=DesignDrawingType.choices,
    )
