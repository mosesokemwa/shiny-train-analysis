import abc
import json
import requests
from lxml.html import fromstring
from jobs.entities import Job
from typing import Generator
import re
from .AbstractProvider import AbstractProvider


class AbstractTokenProvider(AbstractProvider):

    def get_job(self, job_url: str) -> dict:
        content = requests.get(job_url).content
        tree = fromstring(content.decode())
        matches = tree.xpath('//script[@type="application/ld+json"]')
        for match in matches:
            text = re.sub(r'\s+', ' ', match.text)
            text = re.sub(r',\s*(?=[}\]])', '', text)
            element = json.loads(text.strip())
            if type(element) is dict and element["@type"] == 'JobPosting':
                org = element.get("hiringOrganization", {})
                job_dict = {
                    "job_title": element.get("title"),
                    "hiring_organization": org if type(org) is str else org.get("name"),
                    "city": element.get("jobLocation", {}).get("address", {}).get("addressLocality"),
                    "country": element.get("jobLocation", {}).get("address", {}).get("addressRegion"),
                    "employment_type": element.get("employmentType"),
                    "education_requirements": element.get("educationRequirements"),
                    "qualifications": element.get("qualifications"),
                    "experience_requirement": element.get("experienceRequirements"),
                    "industry": element.get("industry"),
                    "date_posted": element.get("datePosted"),
                    "valid_through": element.get("validThrough"),
                    "description": element.get("description"),
                    "skills": element.get("skills"),
                    "responsibilities": element.get("responsibilities"),
                    "value_currency": element.get("salaryCurrency"),
                    "min_value": element.get("baseSalary"),
                    "max_value": element.get("estimatedSalary"),
                    "value_period": None,
                    "instructions": None,
                }
                if hasattr(self, 'post_process'):
                    job_dict = self.post_process(job_dict)
                return job_dict
        return {}

    def get_jobs_list(self, entry_url: str) -> Generator:
        content = requests.get(entry_url).content
        tree = fromstring(content.decode())
        matches = tree.xpath('//script[@type="application/ld+json"]')
        for match in matches:
            text = re.sub(r'\s+', ' ', match.text)
            text = re.sub(r',\s*(?=[}\]])', '', text)
            element = json.loads(text)
            if type(element) is dict and element["@type"] == 'ItemList':
                for child_element in element.get("itemListElement", []):
                    if "url" in child_element:
                        yield child_element.get("url")
                    elif "item" in child_element:
                        yield child_element.get("item").get("url")
                    else:
                        # get confused
                        pass
            else:
                # also get confused
                pass

