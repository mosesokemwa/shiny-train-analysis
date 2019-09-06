from dateutil.parser import parse
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractHTMLProvider import AbstractHTMLProvider


class PNetProvider(AbstractHTMLProvider):
    host = 'pnet.co.za'
    name = 'P Net'
    urls_xpath = "//a[contains(@class, 'job-element__url')]"
    properties = {
        'job_title': "//h1[contains(@class, 'listing__job-title')]",
        'hiring_organization': "//h6[contains(@class, 'listing__company-name')]",
        'city': "//li[contains(@class, 'at-listing__list-icons_location')]/a/span[2]",

        'employment_type': "//li[contains(@class, 'at-listing__list-icons_work-type')]/text()[2]",
        'date_posted': "//span[contains(@class, 'date-time-ago')]/@data-date",
        'valid_through': None,

        'description': "//main[contains(@class, 'offer__content')][section]",

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
        "source": None,
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

            offset = page * 100
            loop_url = entry_url + (f'&of={offset}' if '?' in entry_url else f'?of={offset}')

            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs

    def post_process(self, job_dict):
        # process job posted, process time
        posted = parse(job_dict['date_posted'])
        job_dict['date_posted'] = str(posted)
        return job_dict
