import pytz
from urllib.parse import urljoin
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractHTMLProvider import AbstractHTMLProvider
from jobs.services.scraper.providers.AbstractTokenProvider import AbstractTokenProvider
from datetime import datetime


class EmergeProvider(AbstractHTMLProvider, AbstractTokenProvider):
    timezone = pytz.timezone('Africa/Nairobi')
    host = 'e-merge.co.za'
    name = 'Emerge'
    urls_xpath = "//div[contains(@class, 'et_pb_text_inner')]//a[@class='wpjb-job_title wpjb-title']"

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

            entry_url += '' if entry_url.endswith('/') else '/'
            loop_url = urljoin(entry_url + 'page/', f'{page}/')

            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs
