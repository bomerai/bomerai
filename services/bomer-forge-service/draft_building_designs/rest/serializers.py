from rest_framework import serializers
from draft_building_designs.models import (
    DraftBuildingDesign,
    DesignDrawing,
    DesignDrawingType,
    DesignDrawingPlanType,
    DesignDrawingPlanSubtype,
    DesignDrawingPlan,
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
    design_drawing_plan_type = serializers.ChoiceField(
        choices=DesignDrawingPlanType.choices,
    )
    design_drawing_plan_subtype = serializers.ChoiceField(
        choices=DesignDrawingPlanSubtype.choices,
    )


class DesignDrawingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignDrawingPlan
        fields = "__all__"


class DesignDrawingSerializer(serializers.ModelSerializer):
    design_drawing_plans = DesignDrawingPlanSerializer(many=True)

    class Meta:
        model = DesignDrawing
        fields = "__all__"
