from .entities import JobsList
from urllib.parse import urlparse
from .providers import providers


class JobsService:
    def __init__(self):
        self.providers_service = ProvidersService()

    def fetch_provider(self, job: str) -> JobsList:
        return self.providers_service.fetch_provider(job)

    def fetch_list(self, providers: list) -> JobsList:
        job_list = JobsList()
        for provider in providers:
            job_list.extend(self.fetch_provider(provider))

        return job_list


class ProvidersService:
    def fetch_provider(self, provider: str) -> JobsList:
        parsed = urlparse(provider)
        host = parsed.netloc
        host = host[4:] if host.startswith("www.") else host
        jobs = providers[host].fetch(provider)
        return jobs

