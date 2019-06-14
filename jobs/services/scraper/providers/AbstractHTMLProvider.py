import abc
from lxml.html import fromstring
from jobs.entities import Job
from typing import Generator
from urllib.parse import urljoin, urlparse
from .AbstractProvider import AbstractProvider

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


class AbstractHTMLProvider(AbstractProvider):
    @abc.abstractproperty
    def urls_xpath(self): raise NotImplementedError
    @abc.abstractproperty
    def properties(self): raise NotImplementedError

    def get_job(self, job_url: str) -> Job:
        content = session.get(job_url).content
        tree = fromstring(content.decode())
        job_dict = {}
        for key, value in self.properties.items():
            element, = tree.xpath(value)
            job_dict[key] = ''.join(element.itertext())
        job_dict["source"] = urlparse(job_url).netloc
        if hasattr(self, 'post_process'):
            job_dict = self.post_process(job_dict)
        return job_dict

    def get_jobs_list(self, entry_url: str) -> Generator:
        content = session.get(entry_url).content
        tree = fromstring(content.decode())
        matches = tree.xpath(self.urls_xpath)
        for match in matches:
            job_url = urljoin(entry_url, match.attrib['href'])
            yield job_url