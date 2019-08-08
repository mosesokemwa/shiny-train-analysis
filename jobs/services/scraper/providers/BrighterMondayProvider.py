from datetime import datetime
import pytz
from jobs.models import JobsList
from .AbstractTokenProvider import AbstractTokenProvider


class BrighterMondayProvider(AbstractTokenProvider):
    pagination = 'page'
    host = ['brightermonday.co.ke', 'brightermonday.co.ug', 'brightermonday.co.tz']
    timezone = pytz.timezone("Africa/Nairobi")

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            try:
                page_buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))
        page = 2
        while page_buffer:
            self.jobs.extend(page_buffer)
            page_buffer = []
            loop_url = f'{entry_url}?{self.pagination}={page}'
            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1
        return self.jobs