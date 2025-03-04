from rest_framework import serializers
from draft_building_designs.models import DraftBuildingDesign


class DraftBuildingDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftBuildingDesign
        fields = "__all__"


class CreateDraftBuildingDesignSerializer(serializers.Serializer):
    project_uuid = serializers.UUIDField()
