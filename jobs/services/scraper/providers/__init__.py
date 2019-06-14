from .AbstractProvider import AbstractProvider
from .IHubProvider import IHubProvider
from .BrighterMondayProvider import BrighterMondayProvider
from .CareerPointProvider import CareerPointProvider
from .FuzuProvider import FuzuProvider
from .PigiaMeProvider import PigiaMeProvider
from .JobWebKenyaProvider import JobWebKenyaProvider
from .GlassDoorProvider import GlassDoorProvider
provider_abstract = AbstractProvider.__subclasses__()
providers = {}

for provider_main in provider_abstract:
    for provider in provider_main.__subclasses__():
        host = provider.__dict__.get("host")
        hosts = [host] if type(host) is str else host
        for host in hosts:
            providers[host] = provider()
