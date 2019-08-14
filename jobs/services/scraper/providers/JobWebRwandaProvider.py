
from urllib.parse import urljoin
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractTokenProvider import AbstractTokenProvider
from .AbstractHTMLProvider import AbstractHTMLProvider


class JobWebRwandaProvider(AbstractHTMLProvider, AbstractTokenProvider):
    name = "Jobweb Rwanda"
    host = 'jobwebrwanda.com'
    urls_xpath = '//ol/li/div[2]/strong/a'
    properties = {}

    def get_job(self, job_link):
        return AbstractTokenProvider.get_job(self, job_link)

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            try:
                page_buffer.append(self.get_job(job_link))
            except:
                print("Error Proccessing %s "%job_link)

        page = 2
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            entry_url += '' if entry_url.endswith('/') else '/'
            loop_url = urljoin(entry_url, f'page/{page}/')
            print(loop_url)
            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except:
                    print("Error Proccessing %s " % job_link)

            print("Scraped page %s" % page)
            page += 1

        return self.jobs
