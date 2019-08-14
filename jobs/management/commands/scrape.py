from django.core.management.base import BaseCommand
from jobs.services.scraper.scraper import Scraper, AsyncScraper
from jobs.models import ServerSyncJob

class Command(BaseCommand):
    service=AsyncScraper()
    help = 'Run the scraper.'

    def add_arguments(self, parser):
        parser.add_argument("url",type=str,help="url to scrape. provide 'defaults' for all.")

    def validate_url(self,url):
        return True

    def handle(self, *args, **kwargs):
        url=kwargs["url"]
        if url=="defaults":
            server_sync_job = ServerSyncJob()
            try:
                self.service.fetch_providers_urls()
            except Exception as e:
                server_sync_job.error = True
                server_sync_job.error_message = "%s"%e
            server_sync_job.save()
            return
