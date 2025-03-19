from rest_framework import serializers
from building_components.models import BuildingComponent


class BuildingComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingComponent
        fields = "__all__"
