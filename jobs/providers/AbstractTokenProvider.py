import abc
import json
import requests
from lxml.html import fromstring
from jobs.entities import Job
from typing import Generator
from .AbstractProvider import AbstractProvider


class AbstractTokenProvider(AbstractProvider):
    
    def get_job(self, job_url: str) -> Job:
        content = requests.get(job_url).content
        tree = fromstring(content.decode())
        matches = tree.xpath('//script[@type="application/ld+json"]')
        for match in matches:
            element = json.loads(match.text)
            if element["@type"] == 'JobPosting':
                job = Job(
                    title=element.get("title"),
                )
                return job

        return Job()

    def get_jobs_list(self, entry_url: str) -> Generator:
        content = requests.get(entry_url).content
        tree = fromstring(content.decode())
        matches = tree.xpath('//script[@type="application/ld+json"]')
        for match in matches:
            element = json.loads(match.text)
            if element["@type"] == 'ItemList':
                for child_element in element.get("itemListElement", []):
                    yield child_element.get("url")
            else:
                # get confused
                pass

