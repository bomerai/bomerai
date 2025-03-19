from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from building_components.models import BuildingComponent, BuildingComponentType


class BuildingComponentTypeAdmin(TreeAdmin):
    form = movenodeform_factory(BuildingComponentType)


admin.site.register(BuildingComponentType)
admin.site.register(BuildingComponent)
