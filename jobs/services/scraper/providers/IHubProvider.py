from urllib.parse import urljoin
from jobs.models import JobsList
from .AbstractHTMLProvider import AbstractHTMLProvider
from datetime import datetime
from jobs.services.scraper import country_mapping
import pytz


class IHubProvider(AbstractHTMLProvider):
    host = 'ihub.co.ke'
    urls_xpath = '//h3/a'
    timezone = pytz.timezone('Africa/Nairobi')
    properties = {
        'job_title': "//div[@class='container-fluid job-article-header']/div/h1",
        'hiring_organization': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/a[1]",
        'city': "//div[@class='city-location']",
        'employment_type': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/a[2]",
        'date_posted': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/span[1]",
        'valid_through': "//div[@class='container-fluid job-article-header']/div[1]/ul/li/span[2]",
        'description': "//div[@class='vacancy-description']",
        'instructions': "//div[@class='how-to-apply']",
        "country": None,
        "education_requirements": None,
        "qualifications": None,
        "experience_requirement": None,
        "industry": None,
        "skills": None,
        "responsibilities": None,
        "value_currency": None,
        "min_value": None,
        "max_value":None,
        "url": None,
        "value_period": None,
        "instructions": None,
        "source": None,
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

    def post_process(self, job):
        # you can do field standardization here
        # Ihub gives date in this format '01 Dec, 2018', we need a timestamp
        posted = datetime.strptime(job["date_posted"], "%d %b, %Y")
        posted = self.timezone.localize(posted)
        job["date_posted"] = str(posted)
        posted = datetime.strptime(job["valid_through"], "%d %b, %Y")
        posted = self.timezone.localize(posted)
        job["valid_through"] = str(posted)
        job["city"], job["country"] = job["city"].rsplit(", ")[-2:]
        job["country"] = country_mapping.get(job["country"], job["country"])
        job.update({
            "value_period": None, "education_requirements": None,
            "qualifications": None, "experience_requirement": None,
            "industry": None, "skills": None,
            "responsibilities": None, "value_currency": None,
            "min_value": None, "max_value": None,
        })
        return job
