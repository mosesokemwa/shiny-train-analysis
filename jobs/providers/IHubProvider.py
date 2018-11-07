from urllib.parse import urljoin
from jobs.entities import JobsList
from .AbstractHTMLProvider import AbstractHTMLProvider


class IHubProvider(AbstractHTMLProvider):
    host = 'ihub.co.ke'
    urls_xpath = '//h3/a'
    properties = {
        'job_title': "//div[@class='container-fluid job-article-header']/div/h1",
        'hiring_organization': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/a[1]",
        'city': "//div[@class='city-location']",
        'short_desc': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/a[2]",
        'date_posted': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/span[1]",
        'valid_through': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/span[2]",
        'description': "//div[@class='vacancy-description']",
        'instructions': "//div[@class='how-to-apply']",
    }

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            try:
                page_buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))

        page = 2
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            entry_url += '' if entry_url.endswith('/') else '/'
            loop_url = urljoin(entry_url + '/', f'{page}')

            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))

            page += 1

        return self.jobs
