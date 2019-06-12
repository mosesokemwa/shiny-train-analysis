from datetime import datetime
import pytz
from jobs.entities import JobsList
from .AbstractTokenProvider import AbstractTokenProvider


class PigiaMeProvider(AbstractTokenProvider):
    pagination = 'page'
    host = 'pigiame.co.ke'
    timezone = pytz.timezone('Africa/Nairobi')

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

    def post_process(self, job):
        # you can do field standardization here
        # Glassdoor gives date in this format '2018-12-11', we need a timestamp
        posted = datetime.strptime(job["date_posted"], "%Y-%m-%d")
        posted = self.timezone.localize(posted)
        job["date_posted"] = str(posted)
        posted = datetime.strptime(job["valid_through"], "%Y-%m-%d")
        posted = self.timezone.localize(posted)
        job["valid_through"] = str(posted)
        return job