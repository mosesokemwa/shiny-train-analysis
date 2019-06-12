import os
import json
from jobs.settings import BASE_DIR
from urllib.parse import urlparse
from jobs.services.scraper.providers import providers
from jobs.services.scraper.AbstractScraper import AbstractScraper
from jobs.services.scraper import default_providers_list
from jobs.handlers.cleaner_handler import CleanHtmlHandler
from jobs.handlers.csv_storage_handler import CsvStorageHandler
from jobs.handlers.error_handler import ErrorLogHandler
from jobs.handlers.postgres import PostgresDBHandler


class Scraper(AbstractScraper):
    provider_urls=default_providers_list
    providers=providers
    parser=None
    errorLogHandler=ErrorLogHandler()

    def __init__(self, *args, **kwargs):
        self.db_handler=PostgresDBHandler()
        self.clean_html_handler=CleanHtmlHandler()
        self.csv_storage_handler=CsvStorageHandler()

    def fetch(self,provider_url):
        parsed = urlparse(provider_url)
        host = parsed.netloc
        host = host[4:] if host.startswith("www.") else host
        provider_scraper=providers[host]
        jobs = provider_scraper.fetch(provider_url)
        cleaned_jobs=self.clean_html_handler.clean_data(jobs)
        return host,cleaned_jobs,provider_url

    def fetch_providers_urls(self):
        results=[]
        for name,url in self.provider_urls.items():
            d=self.fetch(url)
            if d:
                results.append(d)
        return results

    def parse(self,host,jobs_list):
        parser=self.providers[host].get_parser()
        return parser.parse_job_list(jobs_list)

    def parse_many(self,jobs_dict):
        results={}
        for host,jobs in jobs_dict.items():
            results[host]=self.parse(host,jobs)
        return results

    def store(self,jobs_list):
            return True

    def store_to_db(self,jobs_list):
        return True

    def store_to_csv(self, host, jobs_list):
        self.csv_storage_handler.write(jobs_list)
        return True

    def store_to_json(self,url,data):
        name=urlparse(url).netloc.replace(".com","").replace("www.","")
        with open(BASE_DIR+"/fixtures/{}.json".format(name),"w") as infile:
            json.dump(data,infile)
        return True

    def set_parser(self,parser):
        self.parser=parser

    def set_provider_urls(self,providers_list):
        self.provider_urls=provider_urls

    def set_providers(self,providers):
        self.providers=providers




