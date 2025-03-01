from django.core.management.base import BaseCommand

from studies.services.ingest_pillars_data import ingest_pillars_with_openai


class Command(BaseCommand):
    help = "Ingest columns data"

    def handle(self, *args, **kwargs):
        ingest_pillars_with_openai()
