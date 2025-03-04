from rest_framework import serializers


class UploadFoundationMetadataSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField())
    building_design_uuid = serializers.UUIDField()
