from django.urls import path

from building_components.rest.views import (
    ingest_foundation_metadata,
)

urlpatterns = [
    path(
        "building-components/ingest-foundation-metadata/",
        ingest_foundation_metadata,
        name="building-components-ingest-foundation-metadata",
    ),
]
