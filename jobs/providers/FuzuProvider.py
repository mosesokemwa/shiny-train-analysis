from jobs.entities import JobsList
from .AbstractTokenProvider import AbstractTokenProvider
from urllib.parse import urlparse, urljoin


class FuzuProvider(AbstractTokenProvider):
    pagination = 'page'
    host = 'fuzu.com'

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []
        scheme_host = urlparse(entry_url)
        scheme_host = scheme_host.scheme + '://' + scheme_host.netloc
        for job_link in self.get_jobs_list(entry_url):
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
            for job_link in self.get_jobs_list(loop_url):
                job_path = urlparse(job_link).path
                job_link = urljoin(scheme_host, job_path)
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs
