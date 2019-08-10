import os
import json
from jobs.settings import BASE_DIR
from urllib.parse import urlparse
from jobs.services.scraper.providers import providers
from jobs.services.scraper.AbstractScraper import AbstractScraper
from jobs.services.scraper import default_providers_list
from jobs.handlers.cleaner_handler import CleanHtmlHandler
from jobs.handlers.error_handler import ErrorLogHandler
from queue import Queue
from threading import Thread


from jobs.services.scraper.storage_handlers import PostgresScraperStorageHandler,CsvScraperStorageHandler,JsonScraperStorageHandler

class Scraper(AbstractScraper):
    provider_urls=default_providers_list
    storage_handlers=[PostgresScraperStorageHandler(),
                    JsonScraperStorageHandler(),
                    CsvScraperStorageHandler()]
    providers=providers
    parser=None
    errorLogHandler=ErrorLogHandler()

    def __init__(self, *args, **kwargs):
        self.clean_html_handler=CleanHtmlHandler()

    def fetch(self,provider_url,store=True):
        try:
            parsed = urlparse(provider_url)
            host = parsed.netloc
            host = host[4:] if host.startswith("www.") else host
            provider_scraper=providers[host]
            jobs = provider_scraper.fetch(provider_url)
            cleaned_jobs=self.clean_html_handler.clean_data(jobs)
            results=[host,cleaned_jobs,provider_url]
            if store==True:
                results[1]=self.parse(results[0],results[1])
                self.store(results)
            return True
        except Exception as e:
            print(e)
            return False

    def fetch_providers_urls(self):
        for name,url in self.provider_urls.items():
            self.fetch(url)
        return True

    def store(self,results):
        for scraper_storage_handler in self.storage_handlers:
            scraper_storage_handler.store(results)
        return True

    def parse(self,host,jobs_list):
        parser=self.providers[host].get_parser()
        if parser:
            return parser.parse_job_list(jobs_list)
        return jobs_list

    def parse_many(self,jobs_dict):
        results=[]
        for i in jobs_dict:
            r=self.parse(i[0],i[1])
            if r:
                results.append((i[0],r,i[2]))
            else:
                results.append(i)
        return results

    def set_provider_urls(self,providers_list):
        self.provider_urls=provider_urls

    def set_providers(self,providers):
        self.providers=providers

    def set_storage_handlers(self,storage_handlers):
        self.storage_handlers=storage_handlers



class UrlQueue(Queue):
    def __init__(self):
        Queue.__init__(self)

class AsyncScraper(Scraper):
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_queue=UrlQueue()
        self.NUM_THREADS=7

    def async_fetch(self):
        while True:
            url =self.url_queue.get()
            self.fetch(url)
            self.url_queue.task_done()
    
    def fetch_providers_urls(self):
        for name,url in self.provider_urls.items():
            self.url_queue.put(url)
        for i in range(self.NUM_THREADS):
            t= Thread(target=self.async_fetch)
            t.daemon=True
            t.start()
        self.url_queue.join()
        return True
    
