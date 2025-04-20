from rest_framework import serializers
from building_components.models import BuildingComponent, BuildingComponentType


class BuildingComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingComponent
        fields = "__all__"


class CreateBuildingComponentSerializer(serializers.Serializer):
    draft_building_design_id = serializers.UUIDField()
    type = serializers.ChoiceField(choices=BuildingComponentType.choices)
    component_data = serializers.JSONField()
