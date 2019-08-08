from django.core.management.base import BaseCommand
from django.conf import settings
import os,json
from jobs.handlers.postgres import PostgresDBHandler
from jobs.services.scraper.providers.AbstractProvider import AbstractProvider
from jobs.models.Provider import Provider

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        provider_abstract = AbstractProvider.__subclasses__()
        providers = {}
        for provider_main in provider_abstract:
            for provider in provider_main.__subclasses__():
                host = provider.__dict__.get("host")
                hosts = [host] if type(host) is str else host
                name=provider().__class__.__name__
                try:
                    provider=Provider.objects.get(name=name)
                    provider.hosts=hosts
                    provider.save()
                except Provider.DoesNotExist:
                    provider=Provider(name=name)
                    provider.hosts=hosts
                    provider.save()
