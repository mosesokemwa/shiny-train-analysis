import abc
import sys
from typing import List,Dict
from jobs.services import JobsService
from jobs.defaults import StorageHandler, providers_list
from jobs.handlers.cleaner_handler import CleanHtmlHandler
from jobs.handlers.csv_storage_handler import CsvStorageHandler
from jobs.parser.ParserHandler import ParserHandler
from jobs.handlers.error_handler import ErrorLogHandler


class AbstractScraper(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractclassmethod
    def injectDepencies(cls) -> bool:
        pass

    @abc.abstractmethod
    def fetch_and_save(self) -> bool:
        pass

    def fetch_to_csv(self) -> bool:
        pass


class Scraper(AbstractScraper,ErrorLogHandler):
    def __init__(self, providers_list:List, *args, **kwargs):
        self.providers_list=providers_list

    @classmethod
    def injectDepencies(cls,jobs_service=None,
                            storage_handler=None,
                            parse_handler=None,
                            csv_storage_handler=None,
                            clean_html_handler=None) -> bool:
        try:
            cls.jobs_service=jobs_service
            cls.storage_handler=storage_handler
            cls.parse_handler=parse_handler
            cls.csv_storage_handler=csv_storage_handler
            cls.clean_html_handler=clean_html_handler
            return True

        except Exception as e:
            ErrorLogHandler().logError(sys.exc_info(), e, True)
            return False

    def fetch_and_save(self) -> bool:
        try:
            jobs = self.jobs_service.fetch_list(self.providers_list)
            for job_list in jobs:
                print("Fetched %s jobs."%len(job_list))
                self.storage_handler.write( self.clean_html_handler.clean_data(job_list))
                print("Stored %s jobs."%len(job_list))
            return True

        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return False
            
    def fetch_to_csv(self) -> bool:
        try:
            jobs=self.storage_handler.fetch_all()
            parsed_data=self.parse_handler.parse_job_list(jobs)
            self.csv_storage_handler.write(parsed_data)
            return True
        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return False




Scraper.injectDepencies(
    jobs_service=JobsService(),
    storage_handler=StorageHandler(),
    parse_handler=ParserHandler(),
    csv_storage_handler=CsvStorageHandler(),
    clean_html_handler=CleanHtmlHandler()
)

scraper=Scraper(providers_list)
# scraper.fetch_and_save()
scraper.fetch_to_csv()
