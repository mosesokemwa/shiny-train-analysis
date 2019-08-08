from datetime import datetime

import pytz

from jobs.models import JobsList
from .AbstractTokenProvider import AbstractTokenProvider
from urllib.parse import urlparse, urljoin


class FuzuProvider(AbstractTokenProvider):
    pagination = 'page'
    host = 'fuzu.com'
    timezone = pytz.timezone("Africa/Nairobi")

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []
        scheme_host = urlparse(entry_url)
        scheme_host = scheme_host.scheme + '://' + scheme_host.netloc

        intial_page_links=[job_link for job_link in self.get_jobs_list(entry_url)]
        for job_link in intial_page_links:
            job_path = urlparse(job_link).path
            job_link = urljoin(scheme_host, job_path)
            try:
                page_buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))

        page = 2
        while page_buffer:
            self.jobs.extend(page_buffer)
            page_buffer = []
            loop_url = f'{entry_url}?{self.pagination}={page}'
            current_page_links=[job_link for job_link in self.get_jobs_list(loop_url)]
            if current_page_links==intial_page_links:
                break
            for job_link in current_page_links:
                job_path = urlparse(job_link).path
                job_link = urljoin(scheme_host, job_path)
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            intial_page_links=current_page_links
            page += 1
        return self.jobs

    def post_process(self, job):
        # I am in charge of standardizing fields across job objects
        # Fuzu's validthrough timestamp is ok but dateposted is not
        posted = datetime.strptime(job["date_posted"], "%Y-%m-%d")
        posted = self.timezone.localize(posted)
        job["date_posted"] = str(posted)
        return job
