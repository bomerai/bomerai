from pathlib import Path

import structlog
from django.core.management.base import BaseCommand

from building_components.models import (
    BuildingComponent,
    BuildingComponentSubType,
    BuildingComponentType,
    BuildingComponentView,
)

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    help = "Ingest CAD walls from data/walls directory"

    def handle(self, *args, **kwargs):
        # Get the project root directory (where manage.py is located)
        project_root = Path(__file__).resolve().parents[3]
        walls_dir = project_root / "data" / "walls"

        if not walls_dir.exists():
            self.stdout.write(self.style.ERROR(f"Directory not found: {walls_dir}"))
            return

        # List all files in the walls directory
        wall_files = [f for f in walls_dir.iterdir() if f.is_file()]

        if not wall_files:
            self.stdout.write(
                self.style.WARNING("No files found in data/walls directory")
            )
            return

        self.stdout.write(self.style.SUCCESS(f"Found {len(wall_files)} files:"))
        for file in wall_files:
            self.stdout.write(f"- {file.name}")

        # -

        for file in wall_files:
            with open(file, "rb") as f:
                from django.core.files import File

                wall = BuildingComponent.objects.create(
                    type=BuildingComponentType.WALL,
                    sub_type=BuildingComponentSubType.EXTERIOR,
                    view=BuildingComponentView.THREE_DIMENSIONAL,
                    image=File(f, name=file.name),
                    component_data={
                        "description": " ".join(
                            file.name.replace(".png", "").split("_")
                        )
                    },
                )
            wall.embedding_vector = BuildingComponent.generate_image_embedding(
                wall.image
            )
            logger.info(
                f"embedding vector for {file.name}",
                embedding_vector=wall.embedding_vector,
            )
            wall.save()
