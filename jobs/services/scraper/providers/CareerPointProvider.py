from datetime import datetime
from urllib.parse import urljoin
import pytz
from jobs.models import JobsList
from .AbstractTokenProvider import AbstractTokenProvider
from .AbstractHTMLProvider import AbstractHTMLProvider


class CareerPointProvider(AbstractHTMLProvider, AbstractTokenProvider):
    name = "Career Point"
    pagination = 'page'
    host = 'careerpointkenya.co.ke'
    properties = None
    urls_xpath = '//header/h2/a'
    timezone = pytz.timezone("Africa/Nairobi")

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            try:
                page_buffer.append(AbstractTokenProvider.get_job(self, job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))
        page = 2
        while page_buffer:
            self.jobs.extend(page_buffer)
            page_buffer = []
            entry_url += '' if entry_url.endswith('/') else '/'
            loop_url = urljoin(entry_url, f'page/{page}/')
            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(AbstractTokenProvider.get_job(self, job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs

    def post_process(self, job):
        # I am in charge of standardizing fields across job objects
        # Fuzu's validthrough timestamp is ok but dateposted is not
        posted = datetime.strptime(job["date_posted"], "%Y-%m-%d")
        posted = self.timezone.localize(posted)
        job["date_posted"] = str(posted)
        return job
