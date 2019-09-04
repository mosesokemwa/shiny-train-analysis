import pytz
from urllib.parse import urljoin
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractHTMLProvider import AbstractHTMLProvider
from jobs.services.scraper.providers.AbstractTokenProvider import AbstractTokenProvider
from datetime import datetime


class GigaJobProvider(AbstractHTMLProvider, AbstractTokenProvider):
    timezone = pytz.timezone('Africa/Nairobi')
    host = 'en-za.gigajob.com'
    name = 'Giga Job'
    urls_xpath = "//section/div/div/h3/a"

    def __init__(self):
        self.jobs = JobsList()

    def get_job(self, job_url: str):
        return AbstractTokenProvider.get_job(self, job_url)

    def fetch(self, entry_url: str):
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            try:
                page_buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))
        page = 2
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            loop_url = entry_url + (f'&page={page}' if '?' in entry_url else f'?page={page}')
            print("Loop url", loop_url)
            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs
