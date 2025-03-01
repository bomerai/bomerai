from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DraftBuildingDesign
from .serializers import DraftBuildingDesignSerializer


class DraftBuildingDesignViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DraftBuildingDesign model providing CRUD operations.
    """

    queryset = DraftBuildingDesign.objects.all()
    serializer_class = DraftBuildingDesignSerializer
    # permission_classes = [IsAuthenticated]
