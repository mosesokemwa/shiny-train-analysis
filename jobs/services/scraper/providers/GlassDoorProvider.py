
from urllib.parse import urljoin
from datetime import datetime
import pytz
from lxml.html import fromstring
from jobs.models import JobsList
from .AbstractTokenProvider import AbstractTokenProvider

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


class GlassDoorProvider(AbstractTokenProvider):
    name = "Glassdoor"
    pagination_xpath = "//li[@class='next']//a"
    host = 'glassdoor.com'
    timezone = pytz.timezone('Africa/Nairobi')
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Ubuntu Chromium/70.0.3538.77 Chrome/70.0.3538.77 Safari/537.36"
    }

    def fetch(self, entry_url: str) -> JobsList:
        self.jobs = JobsList()
        next_url = entry_url
        while next_url:
            content = session.get(next_url, headers=self.headers).content
            for job_url in self.get_urls_from_content(content):
                print(job_url)
                try:
                    self.jobs.append(self.get_job(job_url))
                except Exception as e:
                    print("Error adding job at %s %s" % (job_url, e))
            urls = fromstring(content.decode()).xpath(self.pagination_xpath)
            if urls:
                next_url_element, = urls
                next_url = next_url_element.attrib['href']
                next_url = urljoin(entry_url, next_url)
            else:
                next_url = None
        return self.jobs

    def post_process(self, job):
        # you can do field standardization here
        # Glassdoor gives date in this format '2018-12-11', we need a timestamp
        posted = datetime.strptime(job["date_posted"], "%Y-%m-%d")
        posted = self.timezone.localize(posted)
        job["date_posted"] = str(posted)
        posted = datetime.strptime(job["valid_through"], "%Y-%m-%d")
        posted = self.timezone.localize(posted)
        job["valid_through"] = str(posted)
        return job