from django.contrib import admin

from .models import (
    DesignDrawing,
    DesignDrawingDocument,
    DesignDrawingPlan,
    DraftBuildingDesign,
)

admin.site.register(DraftBuildingDesign)
admin.site.register(DesignDrawing)
admin.site.register(DesignDrawingDocument)
admin.site.register(DesignDrawingPlan)
