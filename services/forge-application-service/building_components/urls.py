from django.urls import path

from building_components.views import building_component_list

urlpatterns = [
    path(
        "building-components/",
        building_component_list,
        name="building-components-list",
    ),
]
