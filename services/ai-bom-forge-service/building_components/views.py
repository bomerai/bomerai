import logging

from rest_framework.response import Response
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


@api_view(["GET"])
def building_component_list(request):
    logger.info("BuildingComponentList list request")
    return Response({"message": "Hello, world!"})
