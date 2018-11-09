from typing import Generator
from jobs.entities import JobsList
from urllib.parse import urlparse
from jobs.providers import providers



class JobsService:
    def __init__(self):
        self.providers_service = ProvidersService()

    def fetch_provider(self, job: str) -> JobsList:
        return self.providers_service.fetch_provider(job)

    def fetch_list(self, providers: list) -> Generator:
        for provider in providers:
            prov_jobs = self.fetch_provider(provider)
            yield prov_jobs


class ProvidersService:
    def fetch_provider(self, provider: str) -> JobsList:
        parsed = urlparse(provider)
        host = parsed.netloc
        host = host[4:] if host.startswith("www.") else host
        jobs = providers[host].fetch(provider)
        return jobs
