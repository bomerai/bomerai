from django.contrib import admin

from .models import DraftBuildingDesign, DraftBuildingDesignBuildingComponent

admin.site.register(DraftBuildingDesign)
admin.site.register(DraftBuildingDesignBuildingComponent)
