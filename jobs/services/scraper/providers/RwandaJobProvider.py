from requests import PreparedRequest
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractTokenProvider import AbstractTokenProvider
from .AbstractHTMLProvider import AbstractHTMLProvider


class RwandaJobProvider(AbstractHTMLProvider, AbstractTokenProvider):
    name = "RwandaJob"
    host = 'rwandajob.com'
    urls_xpath = "//div[@class='job-search-result  ']/div/div/h5/a"
    properties = {}

    def get_job(self, job_link):
        return AbstractTokenProvider.get_job(self, job_link)

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            try:
                page_buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error Processing %s %s " % (job_link, e))

        page = 1
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            prep_url = PreparedRequest()
            prep_url.prepare(url=entry_url, params={'page': page})
            next_page_url = prep_url.url

            for job_link in self.get_jobs_list(next_page_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error Processing %s %s " % (job_link, e))

            print("Scraped page %s" % page)
            page += 1

        return self.jobs
