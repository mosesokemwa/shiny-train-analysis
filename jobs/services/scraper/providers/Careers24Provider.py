import pytz
from jobs.models import JobsList
from jobs.services.scraper.providers.AbstractHTMLProvider import AbstractHTMLProvider
from datetime import datetime


class Careers24Provider(AbstractHTMLProvider):
    timezone = pytz.timezone('Africa/Nairobi')
    host = 'careers24.com'
    name = 'Careers 24'
    urls_xpath = "//a[@data-trigger='jobalertmodal']"
    properties = {
        'job_title': "//meta[@property='og:title']/@content",
        'hiring_organization': "//span[@class='posted']/span/span",
        'city': "//a[@id='ctl00_contentPrimaryPlaceHolder_NewJobDetail_NewJobSummary_hlLocation']",
        'employment_type': "//ul[@class='job-detail-summary']/li[6]/span/span",
        'date_posted': "//span[@class='posted']/text()",
        'valid_through': "//span[contains(text(), 'Apply before')]/span[1]",

        'description': "//div[@class='job_detail_container']",

        'instructions': "//div[@id='ctl00_contentPrimaryPlaceHolder__ctrl_0_divCandReq']",
        "country": None,
        "education_requirements": None,
        "qualifications": None,
        "experience_requirement": None,
        "industry": "//span[contains(text(),'Sectors:')]/following-sibling::a",
        "skills": "//div[@id='ctl00_contentPrimaryPlaceHolder__ctrl_0_divCandSkills']",
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
        page = 2
        while len(page_buffer) > 0:
            self.jobs.extend(page_buffer)
            page_buffer = []

            loop_url = entry_url + (f'&page={page}' if '?' in entry_url else f'?page={page}')
            print("Next page", loop_url)

            for job_link in self.get_jobs_list(loop_url):
                try:
                    page_buffer.append(self.get_job(job_link))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_link, e))
            page += 1

        return self.jobs

    def post_process(self, job_dict):
        # process job posted, process time
        try:
            posted = datetime.strptime(job_dict['date_posted'], 'on %A, %B %d, %Y')
        except ValueError:
            posted = datetime.strptime(job_dict['date_posted'], 'Posted on %A, %B %d, %Y')
        posted = self.timezone.localize(posted)
        job_dict['date_posted'] = str(posted)
        valid_through = datetime.strptime(job_dict['valid_through'], '%A, %B %d, %Y')
        valid_through = self.timezone.localize(valid_through)
        job_dict['valid_through'] = str(valid_through)
        return job_dict
