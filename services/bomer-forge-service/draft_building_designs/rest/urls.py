from django.urls import path, include
from rest_framework.routers import DefaultRouter
from draft_building_designs.rest.views import (
    DraftBuildingDesignViewSet,
    DesignDrawingComponentMetadataViewSet,
)

router = DefaultRouter()
router.register(
    r"draft-building-designs",
    DraftBuildingDesignViewSet,
    basename="draft-building-designs",
)
router.register(
    r"design-drawing-component-metadata",
    DesignDrawingComponentMetadataViewSet,
    basename="design-drawing-component-metadata",
)

urlpatterns = [
    path("", include(router.urls)),
]
