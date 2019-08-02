import abc
from jobs.services.scraper.parser.ParserHandler import ParserHandler

class AbstractProvider(abc.ABC):
    
    def get_parser(self):
        return ParserHandler()