from django.core.management.base import BaseCommand
from draft_building_designs.models import DXFDocument
from draft_building_designs.embeddings import EmbeddingsGenerator


class Command(BaseCommand):
    help = "Generate embedding vectors for a drawing design"

    def handle(self, *args, **kwargs):
        embeddings_generator = EmbeddingsGenerator()
