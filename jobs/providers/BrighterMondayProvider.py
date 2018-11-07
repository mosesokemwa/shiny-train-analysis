from jobs.entities import JobsList
from .AbstractTokenProvider import AbstractTokenProvider


class BrighterMondayProvider(AbstractTokenProvider):
    pagination = 'page'
    host = 'brightermonday.co.ke'

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            page_buffer.append(self.get_job(job_link))

        page = 2
        while page_buffer:
            self.jobs.extend(page_buffer)
            page_buffer = []
            loop_url = f'{entry_url}?{self.pagination}={page}'
            for job_link in self.get_jobs_list(loop_url):
                page_buffer.append(self.get_job(job_link))
            page += 1

        return self.jobs
