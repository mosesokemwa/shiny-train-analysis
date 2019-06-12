
from urllib.parse import urljoin
from jobs.entities import JobsList
from .AbstractHTMLProvider import AbstractHTMLProvider


class JobWebKenyaProvider(AbstractHTMLProvider):
    host = 'jobwebkenya.com'
    urls_xpath = '//ol/li/div[2]/strong/a'
    properties = {
        'job_title': "//h1[@class='title']",
        'hiring_organization': "",
        'company': "//div[@class='section_content']/ul/li[1]/a",
        'city': "//div[@class='section_content']/ul/li[3]/a",
        'country': "//div[@class='section_content']/ul/li[2]",
        'employment_type': "//div[@class='section_content']/ul/li[4]/span",
        'posted': "//div[@class='date']/strong",
        'date_posted': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/span[2]",
        'full_desc': "//font[@size='2']",
        'instructions': "//font[@size='3']",
    }

    def fetch(self, entry_url: str) -> JobsList:
        print("Warning JobWebKenya is in beta support! Expect Errors!")
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
            loop_url = urljoin(entry_url + '/', f'{page}')

            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except:
                    print("Error Proccessing %s " % job_link)

            print("Scraped page %s" % page)
            page += 1

        return self.jobs