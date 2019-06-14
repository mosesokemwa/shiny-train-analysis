from django.core.management.base import BaseCommand
from django.conf import settings
import os,json
from jobs.handlers.postgres import PostgresDBHandler
from jobs.services.scraper.scraper import Scraper
from jobs.entities.JobListing import JobListing

postgres_db_handler=PostgresDBHandler()

class Command(BaseCommand):
    service=Scraper()
    help = 'Add odds providers to DB'

    def add_arguments(self, parser):
        parser.add_argument("url",type=str,help="url to scrape")

    def validate_url(self,url):
        return True

    def handle(self, *args, **kwargs):
        url=kwargs["url"]
        # self.stdout.write(self.style.SUCCESS
        if url=="defaults":
            data=self.service.fetch_providers_urls()
            data=self.service.parse_many(data)
            if data:
                for d in data:
                    self.service.store_to_json(d[2],d[1])
                    j=JobListing(meta=d[1])
                    if "job_title" in list(d[1].keys()):
                        j.name=d[1]["job_title"]
                    j.save()
                    self.stdout.write(self.style.SUCCESS("Adding {}".format(d[0])))
            return 
                