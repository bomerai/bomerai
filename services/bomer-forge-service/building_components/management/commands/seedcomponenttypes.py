from django.core.management.base import BaseCommand
from building_components.models import BuildingComponentType


class Command(BaseCommand):
    help = "Seed the building component types"

    def handle(self, *args, **kwargs):
        get = lambda node_id: BuildingComponentType.objects.get(pk=node_id)  # noqa

        # root types
        foundation = BuildingComponentType.add_root(
            name="Foundation",
            description="The foundation of the building",
        )
        BuildingComponentType.add_root(
            name="Column", description="The column of the building"
        )
        BuildingComponentType.add_root(
            name="Beam",
            description="The beam of the building",
        )
        BuildingComponentType.add_root(
            name="Slab",
            description="The slab of the building",
        )

        # second level types
        footing = get(foundation.pk).add_child(
            name="Footing",
            description="The footing of the building",
        )
        get(footing.pk).add_child(
            name="Continuous",
            description="The continuous footing of the building",
        )
        get(footing.pk).add_child(
            name="Isolated",
            description="The isolated footing of the building",
        )
