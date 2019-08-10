from django.core.management.base import BaseCommand
from django.conf import settings
import os,json
from jobs.handlers.postgres import PostgresDBHandler
from jobs.services.scraper.scraper import Scraper, AsyncScraper
from jobs.models.JobListing import JobListing

postgres_db_handler=PostgresDBHandler()

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
            self.service.fetch_providers_urls()
            # data=self.service.parse_many(data)
            # if data:
            #     for d in data:
            #         try:
            #             self.service.store_to_json(d[2],d[1])
            #             self.service.store_to_csv(d[2],d[1])
            #             self.service.store_to_db(d)
            #             self.stdout.write(self.style.SUCCESS("Adding {}".format(d[0])))
            #         except Exception as e:
            #             self.stdout.write(self.style.ERROR("Error:%s" %e))
            return
