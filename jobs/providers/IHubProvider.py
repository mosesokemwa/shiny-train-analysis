from urllib.parse import urljoin
from jobs.entities import JobsList
from .AbstractHTMLProvider import AbstractHTMLProvider


class IHubProvider(AbstractHTMLProvider):
    host = 'ihub.co.ke'
    urls_xpath = '//h3/a'
    properties = {
        'title': "//div[@class='container-fluid job-article-header']/div/h1",
        'company': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/a[1]",
        'short_desc': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/a[2]",
        'posted': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/span[1]",
        'deadline': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/span[2]",
        'full_desc': "//div[@class='vacancy-description']",
        'instructions': "//div[@class='how-to-apply']",
    }

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            page_buffer.append(self.get_job(job_link))

        page = 2
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            entry_url += '' if entry_url.endswith('/') else '/'
            loop_url = urljoin(entry_url + '/', f'{page}')

            for job_link in self.get_jobs_list(loop_url):
                page_buffer.append(self.get_job(job_link))
            page += 1

        return self.jobs
