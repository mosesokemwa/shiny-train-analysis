from .AbstractProvider import AbstractProvider
from .IHubProvider import IHubProvider
from .BrighterMondayProvider import BrighterMondayProvider

provider_abstract = AbstractProvider.__subclasses__()

providers = {}

for provider_main in provider_abstract:
    for provider in provider_main.__subclasses__():
        providers[provider.host] = provider()

