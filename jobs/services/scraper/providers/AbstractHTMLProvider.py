from lxml.html import fromstring
from jobs.models import Job
from typing import Generator
from urllib.parse import urljoin, urlparse
from .AbstractProvider import AbstractProvider


class AbstractHTMLProvider(AbstractProvider):

    def get_urls_xpath(self):
        if hasattr(self, 'urls_xpath'):
            return self.urls_xpath
        raise NotImplementedError

    def get_properties(self):
        if hasattr(self, 'properties'):
            return self.properties
        raise NotImplementedError

    def get_job(self, job_url: str) -> Job:
        print("Fetching Job: {}".format(job_url))
        content = self.get_page(job_url).content
        tree = fromstring(content.decode())
        job_dict = {}

        for key, value in self.get_properties().items():
            if value is None:
                job_dict[key] = None
                continue
            element = next(iter(tree.xpath(value)), None)
            if isinstance(element, str):
                job_dict[key] = str(element).strip()
            elif element is None:
                job_dict[key] = None
            else:
                job_dict[key] = ''.join(element.itertext()).strip()

        job_dict["url"] = job_url
        job_dict["source"] = urlparse(job_url).netloc

        if hasattr(self, 'post_process'):
            job_dict = self.post_process(job_dict)
        return job_dict

    def get_jobs_list(self, entry_url: str) -> Generator:
        content = self.get_page(entry_url).content
        tree = fromstring(content.decode())
        matches = tree.xpath(self.get_urls_xpath())
        for match in matches:
            job_url = urljoin(entry_url, match.attrib['href'])
            yield job_url
