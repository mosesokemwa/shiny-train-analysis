import abc

class AbstractScraper(abc.ABC):
    
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def fetch(self,provider_url):
        pass

    @abc.abstractmethod
    def parse(self,jobs_list):
        pass

    @abc.abstractmethod
    def store(self,jobs_list):
        pass

    @abc.abstractmethod
    def set_parser(self,parser):
        pass

    @abc.abstractmethod
    def set_provider_urls(self,providers_list):
        pass

    @abc.abstractmethod
    def set_providers(self,providers):
        pass