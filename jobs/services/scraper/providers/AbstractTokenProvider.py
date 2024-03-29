import re
import json
from urllib.parse import urlparse
from jobs.services.scraper import country_mapping
from lxml.html import fromstring
from typing import Generator
from .AbstractProvider import AbstractProvider


class AbstractTokenProvider(AbstractProvider):
    headers = {}

    def parse_job_from_content(self, content: bytes, job_url: str) -> dict:
        tree = fromstring(content.decode())
        matches = tree.xpath('//script[@type="application/ld+json"]')
        for match in matches:
            text = re.sub(r'\s+', ' ', match.text)
            text = re.sub(r',\s*(?=[}\]])', '', text)
            element = json.loads(text.strip())
            if type(element) is dict and "@type" in element and element["@type"] == 'JobPosting':
                org = element.get("hiringOrganization", {})
                country = None
                address = element.get("jobLocation", {}).get("address")
                if address:
                    if address["@type"] == "PostalAddress":
                        country = address.get("addressCountry")
                        if type(country) is dict:
                            country = country.get("name")
                        country = country_mapping.get(country)
                    else:
                        pass
                job_dict = {
                    "job_title": element.get("title"),
                    "hiring_organization": org if type(org) is str else org.get("name"),
                    "city": element.get("jobLocation", {}).get("address", {}).get("addressLocality"),
                    "country": country,
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
                    "url": job_url,
                    "value_period": None,
                    "instructions": None,
                    "source": urlparse(job_url).netloc,
                }
                if hasattr(self, 'post_process'):
                    job_dict = self.post_process(job_dict)
                return job_dict
        raise Exception("\nNo Job Found on Page")

    def get_urls_from_content(self, content: bytes) -> Generator:
        tree = fromstring(content.decode())
        matches = tree.xpath('//script[@type="application/ld+json"]')
        found_urls=[]
        repeat=False
        for match in matches:
            if repeat:break
            text = re.sub(r'\s+', ' ', match.text)
            text = re.sub(r',\s*(?=[}\]])', '', text)
            element = json.loads(text)
            if type(element) is dict and element["@type"] == 'ItemList':
                for child_element in element.get("itemListElement", []):
                    if "url" in child_element:
                        url=child_element.get("url")
                    elif "item" in child_element:
                        url=child_element.get("item").get("url")
                    else:
                        # list item has no url :-(
                        continue
                    # if url in found_urls:
                    #     print("REPEAT")
                    #     repeat=True
                    #     break
                    found_urls.append(url)
                    yield url
            else:
                # item is not a list :-(
                pass

    def get_job(self, job_url: str) -> dict:
        print("Fetching Job: {}".format(job_url))
        content = self.get_page(job_url, headers=self.headers).content
        return self.parse_job_from_content(content, job_url)

    def get_jobs_list(self, entry_url: str) -> Generator:
        print("Fetching Jobs List: {}".format(entry_url))
        content = self.get_page(entry_url, headers=self.headers).content
        yield from self.get_urls_from_content(content)
