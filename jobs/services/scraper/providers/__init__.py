from .AbstractProvider import AbstractProvider
from .IHubProvider import IHubProvider
from .BrighterMondayProvider import BrighterMondayProvider
from .CareerPointProvider import CareerPointProvider
from .FuzuProvider import FuzuProvider
from .PigiaMeProvider import PigiaMeProvider
from .JobWebProvider import JobWebProvider
from .GlassDoorProvider import GlassDoorProvider
from .RwandaJobProvider import RwandaJobProvider
from .Careers24Provider import Careers24Provider
from .BestJobsProvider import BestJobsProvider
from .EmergeProvider import EmergeProvider
from .GigaJobProvider import GigaJobProvider
from .JobMailProvider import JobMailProvider
from .PNetProvider import PNetProvider
from .JobVineProvider import JobVineProvider
from .JobsInGhanaProvider import JobsInGhanaProvider
from .JobberManProvider import JobberManProvider

provider_abstract = AbstractProvider.__subclasses__()
providers = {}

for provider_main in provider_abstract:
    for provider in provider_main.__subclasses__():
        host = provider.__dict__.get("host")
        hosts = [host] if type(host) is str else host
        for host in hosts:
            providers[host] = provider()
