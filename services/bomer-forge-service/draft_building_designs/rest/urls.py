from django.urls import path, include
from rest_framework.routers import DefaultRouter
from draft_building_designs.rest.views import DraftBuildingDesignViewSet

router = DefaultRouter()
router.register(
    r"draft-building-designs",
    DraftBuildingDesignViewSet,
    basename="draft-building-designs",
)

urlpatterns = [
    path("", include(router.urls)),
]
