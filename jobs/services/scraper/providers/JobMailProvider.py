import pytz
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractHTMLProvider import AbstractHTMLProvider
from jobs.services.scraper.providers.AbstractTokenProvider import AbstractTokenProvider


class JobMailProvider(AbstractHTMLProvider, AbstractTokenProvider):
    timezone = pytz.timezone('Africa/Nairobi')
    host = 'jobmail.co.za'
    name = 'Job Mail'
    urls_xpath = "//a[contains(@class, 'btnView')]"

    def __init__(self):
        self.jobs = JobsList()

    def get_job(self, job_url: str):
        return AbstractTokenProvider.get_job(self, job_url)

    def fetch(self, entry_url: str):
        print(entry_url)
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            print(job_link)
            try:
                page_buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))
        page = 2
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            loop_url = entry_url.rsplit('/', 1)[0] + f'/page{page}'

            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs
