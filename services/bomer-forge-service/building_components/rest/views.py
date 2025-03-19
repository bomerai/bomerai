from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from building_components.models import BuildingComponent
from building_components.rest.serializers import BuildingComponentSerializer


class BuildingComponentViewSet(ModelViewSet):
    queryset = BuildingComponent.objects.all()
    serializer_class = BuildingComponentSerializer
    permission_classes = [IsAuthenticated]
