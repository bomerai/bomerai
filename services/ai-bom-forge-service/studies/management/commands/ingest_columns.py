from django.core.management.base import BaseCommand

from studies.services.ingest_pillars_data import (
    ingest_pillars_data,
    ingest_pillars_with_openai,
)
from studies.services.ingest_pillars_data_with_ocr import ingest_pillars_with_ocr


class Command(BaseCommand):
    help = "Ingest columns data"

    def handle(self, *args, **kwargs):
        # ingest_pillars_with_ocr()
        ingest_pillars_with_openai()
