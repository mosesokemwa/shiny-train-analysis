import pytz
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractHTMLProvider import AbstractHTMLProvider
from datetime import datetime


class JobsInGhanaProvider(AbstractHTMLProvider):
    timezone = pytz.timezone('Africa/Nairobi')
    host = 'jobsinghana.com'
    name = 'Jobs Ghana'
    urls_xpath = "//a[@property='title']"
    properties = {
        'job_title': "//div[@class='jobdetailtitle']/h3",
        'hiring_organization': "//td[text()='Company']/following-sibling::td/@title",

        'city': "//td[text()='Location']/following-sibling::td/@title",
        'employment_type': "//td[text()='Job Status']/following-sibling::td/@title",
        'date_posted': None,
        'valid_through': "//td[text()='Job Expires']/following-sibling::td/@title",

        'description': "//td[@class='job_desc']",

        'instructions': None,
        "country": None,
        "education_requirements": None,
        "qualifications": None,
        "experience_requirement": "//td[text()='Experience']/following-sibling::td/@title",
        "industry": "//td[text()='Industry']/following-sibling::td/@title",
        "skills": None,
        "responsibilities": None,
        "value_currency": None,
        "min_value": None,
        "max_value": None,
        "url": None,
        "value_period": None,
        "source": None
    }

    def __init__(self):
        self.jobs = JobsList()

    def fetch(self, entry_url: str):
        self.jobs = JobsList()
        page_buffer = []

        for job_link in self.get_jobs_list(entry_url):
            try:
                page_buffer.append(self.get_job(job_link))
            except Exception as e:
                print("Error adding job at %s %s" % (job_link, e))
        page = 1
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            loop_url = entry_url + (f'&page={page}' if '?' in entry_url else f'?page={page}')

            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs

    def post_process(self, job_dict):
        # process job posted, process time
        # Sep 16, 2019
        posted = datetime.strptime(job_dict['valid_through'], '%b %d, %Y')
        posted = self.timezone.localize(posted)
        job_dict['valid_through'] = str(posted)
        return job_dict
