from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    """

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["created_by", "updated_by"]
