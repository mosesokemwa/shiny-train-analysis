import abc
import requests
from lxml.html import fromstring
from jobs.entities import Job
from typing import Generator
from urllib.parse import urljoin, urlparse
from .AbstractProvider import AbstractProvider


class AbstractHTMLProvider(AbstractProvider):
    @abc.abstractproperty
    def urls_xpath(self): raise NotImplementedError
    @abc.abstractproperty
    def properties(self): raise NotImplementedError

    def get_job(self, job_url: str) -> Job:
        content = requests.get(job_url).content
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
        content = requests.get(entry_url).content
        tree = fromstring(content.decode())
        matches = tree.xpath(self.urls_xpath)
        for match in matches:
            job_url = urljoin(entry_url, match.attrib['href'])
            yield job_url

