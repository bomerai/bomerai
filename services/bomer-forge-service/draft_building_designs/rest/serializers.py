from rest_framework import serializers
from draft_building_designs.models import (
    DraftBuildingDesign,
    DraftBuildingDesignBuildingComponent,
    DraftBuildingDesignCalculationModule,
)
from building_components.rest.serializers import BuildingComponentSerializer


class DraftBuildingDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftBuildingDesign
        fields = "__all__"


class CreateDraftBuildingDesignSerializer(serializers.Serializer):
    project_uuid = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()


class UploadDesignDrawingSerializer(serializers.Serializer):
    draft_building_design_uuid = serializers.UUIDField()
    files = serializers.ListField(child=serializers.FileField())
    type = serializers.ChoiceField(choices=["FOOTING", "COLUMN", "BEAM", "SLAB"])


class DraftBuildingDesignBuildingComponentSerializer(serializers.ModelSerializer):
    building_component = BuildingComponentSerializer()

    class Meta:
        model = DraftBuildingDesignBuildingComponent
        fields = "__all__"


class DraftBuildingDesignCalculationModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftBuildingDesignCalculationModule
        fields = "__all__"


class DraftBuildingDesignBomItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    steel_weight = serializers.FloatField()
    concrete_volume = serializers.FloatField()
    quantity = serializers.IntegerField()


class DraftBuildingDesignBomSerializer(serializers.Serializer):
    footings = DraftBuildingDesignBomItemSerializer(many=True)
    columns = DraftBuildingDesignBomItemSerializer(many=True)
    beams = DraftBuildingDesignBomItemSerializer(many=True)
    slabs = DraftBuildingDesignBomItemSerializer(many=True)
