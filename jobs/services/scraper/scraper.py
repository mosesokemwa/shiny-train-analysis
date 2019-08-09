import os
import json
import hashlib
from jobs.settings import BASE_DIR
from urllib.parse import urlparse
from jobs.services.scraper.providers import providers
from jobs.services.scraper.AbstractScraper import AbstractScraper
from jobs.services.scraper import default_providers_list
from jobs.handlers.cleaner_handler import CleanHtmlHandler
from jobs.handlers.csv_storage_handler import CsvStorageHandler
from jobs.handlers.error_handler import ErrorLogHandler
from jobs.handlers.postgres import PostgresDBHandler
from jobs.models.JobListing import JobListing
from threading import Thread
import dateutil.parser


from jobs.models import JobListing,HiringOrganization,Provider

class ScraperStorageHandler:

    def save_jobs_list_to_db(self, results):
        provider_name=providers[results[0]].__class__.__name__
        provider=Provider.objects.get(name=provider_name)
        for job in results[1]:
            try:
                hiring_organization = HiringOrganization.objects.get(name=job["hiring_organization"])
            except HiringOrganization.DoesNotExist:
                hiring_organization=HiringOrganization(name=job["hiring_organization"])
                hiring_organization.save()
            except Exception as e:
                hiring_organization=None

            job_dict=dict(
                title=job["job_title"],
                provider=provider,
                hiring_organization=hiring_organization,
                location=job["city"] if type(job["city"])==str else "" + " " + job["country"] if type(job["country"])==str else "",
                skills= [i for i in job["skills"].split("\n") if i != "" and type(i) == str ] if job["skills"] != None else None,
                tags=[i for i in job["tags"].split(",") if type(i)==str and i !=""] if job["tags"] != None else None,
                employment_type=job["employment_type"],
                date_posted=dateutil.parser.parse(job["date_posted"]),
                valid_to=dateutil.parser.parse(job["valid_through"]),
                url=job["url"],
                industry=job["industry"] if type(job["industry"]) == str else None,
                description=job["description"] if type(job["description"]) == str else "",
                education_requirements=job["education_requirements"] if type(job["education_requirements"]) == str else "",
                qualifications=job["qualifications"] if type(job["qualifications"]) == str else "",
                responsibilities=job["responsibilities"] if type(job["responsibilities"]) == str else "",
                instructions=job["instructions"] if type(job["instructions"]) == str else "",
            )

            try:
                job_=JobListing.objects.get(url=job["url"])
                for attr,value in job_dict.items():
                    setattr(job_,attr,value)
                job_.save()

            except JobListing.DoesNotExist:
                job_=JobListing(**job_dict)
                job_.save()
                
            except Exception as e:
                print(e)
        return True

class Scraper(AbstractScraper):
    provider_urls=default_providers_list
    providers=providers
    parser=None
    errorLogHandler=ErrorLogHandler()
    db_storage_handler=ScraperStorageHandler()

    def __init__(self, *args, **kwargs):
        self.db_handler=PostgresDBHandler()
        self.clean_html_handler=CleanHtmlHandler()
        self.csv_storage_handler=CsvStorageHandler()

    def fetch(self,provider_url):
        try:
            parsed = urlparse(provider_url)
            host = parsed.netloc
            host = host[4:] if host.startswith("www.") else host
            provider_scraper=providers[host]
            jobs = provider_scraper.fetch(provider_url)
            cleaned_jobs=self.clean_html_handler.clean_data(jobs)
            return host,cleaned_jobs,provider_url
        except Exception as e:
            print(e)
            return False

    def fetch_providers_urls(self):
        results=[]
        for name,url in self.provider_urls.items():
            d=self.fetch(url)
            if d:
                results.append(d)
        return results

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

    def store(self,jobs_list):
        
        return True

    def store_to_db(self,jobs_list):
        return self.db_storage_handler.save_jobs_list_to_db(jobs_list)

    def store_to_csv(self,url,data):
        name=urlparse(url).netloc.replace(".com","").replace("www.","")
        path=BASE_DIR+"/fixtures/{}.csv".format(name)
        return self.csv_storage_handler.write(path,data)

    def store_to_json(self,url,data):
        name=urlparse(url).netloc.replace("www.","")
        with open(BASE_DIR+"/fixtures/{}.json".format(name),"w") as infile:
            json.dump(data,infile)
        return True

    def set_parser(self,parser):
        self.parser=parser

    def set_provider_urls(self,providers_list):
        self.provider_urls=provider_urls

    def set_providers(self,providers):
        self.providers=providers




from queue import Queue

class UrlQueue(Queue):
    def __init__(self):
        Queue.__init__(self)

class DataQueue(Queue):
    def __init__(self):
        Queue.__init__(self)


class AsyncScraper(Scraper):
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_queue=UrlQueue()
        self.data_queue=DataQueue()
        self.NUM_THREADS=5
        self.results=[]
    
    def async_fetch(self):
        while True:
            url =self.url_queue.get()
            data=self.fetch(url)
            if data:
                self.data_queue.put(data)
            self.url_queue.task_done()
    
    def fetch_providers_urls(self):
        for name,url in self.provider_urls.items():
            self.url_queue.put(url)
        
        for i in range(self.NUM_THREADS):
            t= Thread(target=self.async_fetch)
            t.daemon=True
            t.start()
        self.url_queue.join()
        results=list(self.data_queue.queue)
        return results
    
