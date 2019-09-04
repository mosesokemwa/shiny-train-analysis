import pytz
from jobs.models import JobsList
from .AbstractTokenProvider import AbstractTokenProvider


class BrighterMondayProvider(AbstractTokenProvider):
    name = "Brighter Monday"
    pagination = 'page'
    host = ['brightermonday.co.ke', 'brightermonday.co.ug', 'brightermonday.co.tz']
    timezone = pytz.timezone("Africa/Nairobi")

    def __init__(self):
        self.jobs = JobsList()

    def fetch_page(self, page_url):
        buffer = []

        for job_link in self.get_jobs_list(page_url):
            try:
                buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))

        return buffer

    def fetch(self, entry_url: str) -> JobsList:
        page_buffer = self.fetch_page(entry_url)
        self.jobs = JobsList()
        page = 2
        while page_buffer:
            self.jobs.extend(page_buffer)
            loop_url = f'{entry_url}?{self.pagination}={page}'
            page_buffer = self.fetch_page(loop_url)
            page += 1

        return self.jobs
