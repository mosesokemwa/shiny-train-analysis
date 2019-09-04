import abc
from jobs.services.scraper.parser.ParserHandler import ParserHandler
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


class AbstractProvider(abc.ABC):

    def get_parser(self):
        return ParserHandler()

    def get_page(self, url, **kwargs):
        return session.get(url, **kwargs)
