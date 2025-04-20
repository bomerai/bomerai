from django.contrib import admin

from building_components.models import BuildingComponent


class BuildingComponentAdmin(admin.ModelAdmin):
    list_display = ("uuid", "type", "description", "created_at", "updated_at")
    list_filter = ("type",)
    search_fields = ("uuid", "description")


admin.site.register(BuildingComponent, BuildingComponentAdmin)
