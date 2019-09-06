import pytz
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractHTMLProvider import AbstractHTMLProvider
from datetime import datetime


class JobVineProvider(AbstractHTMLProvider):
    timezone = pytz.timezone('Africa/Nairobi')
    host = 'jobvine.co.za'
    name = 'Job Vine'
    urls_xpath = "//p[contains(@class, 'job-title')]/a"
    properties = {
        'job_title': "//h1[@class='job-title']",
        'hiring_organization': "//span[text()='Recruiter:']/following-sibling::strong",

        'city': "//span[text()='Location:']/following-sibling::strong",
        'employment_type': "//span[text()='Job Type:']/following-sibling::strong",
        'date_posted': "//span[text()='Date added:']/following-sibling::strong",
        'valid_through': None,

        'description': "//div[@class='job-item premium']/following-sibling::div[1]",

        'instructions': None,
        "country": None,
        "education_requirements": None,
        "qualifications": None,
        "experience_requirement": None,
        "industry": None,
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
        posted = datetime.strptime(job_dict['date_posted'], '%d %B %Y')
        posted = self.timezone.localize(posted)
        job_dict['date_posted'] = str(posted)
        return job_dict
