from rest_framework.routers import DefaultRouter
from building_components.rest.views import BuildingComponentViewSet

router = DefaultRouter()
router.register(
    r"building-components", BuildingComponentViewSet, basename="building-components"
)

urlpatterns = router.urls
