from django.core.management.base import BaseCommand
from draft_building_designs.services.pt_pt.extract_drawing_design_files_metadata import (
    extract_footing_metadata,
)
from draft_building_designs.models import DesignDrawingDocument


class Command(BaseCommand):
    help = "Extract metadata from drawing documents"

    def handle(self, *args, **options):
        drawing_document = DesignDrawingDocument.objects.order_by("-created_at").first()
        footing_metadata = extract_footing_metadata(
            drawing_document_uuid=str(drawing_document.uuid)
        )
        print(footing_metadata)
