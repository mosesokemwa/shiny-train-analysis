from urllib.parse import urljoin
from jobs.entities import JobsList
from .AbstractTokenProvider import AbstractTokenProvider


class GlassDoorKigaliProvider(AbstractTokenProvider):
    pagination = ''
    host = 'glassdoor.com'

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
            # entry_url += '' if entry_url.endswith('/') else '/'
            loop_url = entry_url[:-4] + f'{page}.htm'
            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs
