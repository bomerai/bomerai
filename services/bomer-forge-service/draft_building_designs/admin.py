from django.contrib import admin

from .models import (
    DraftBuildingDesign,
    DraftBuildingDesignBuildingComponent,
    DXFEntity,
)

admin.site.register(DraftBuildingDesign)
admin.site.register(DraftBuildingDesignBuildingComponent)
admin.site.register(DXFEntity)
