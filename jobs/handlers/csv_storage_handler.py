import csv
import os
import sys
from typing import List,Dict
from jobs.handlers.abstract_storage_handler import AbstractStorageInterface
from jobs import settings
from jobs.handlers.error_handler import ErrorLogHandler


class CsvConfig:
    pass

class CsvStorageHandler(AbstractStorageInterface,ErrorLogHandler):

    def __init__(self, *args, **kwargs):
        self.FIELDS=["id","job_title","city","hiring_organization","employment_type","months","date_posted","valid_through","tags","source"]


    def write(self,file_path,data:List[Dict]) -> bool:
        try:
            k=[i for i in data[0].keys() if i in self.FIELDS]
            x = [{f:v for f,v in element.items() if f in k} for element in data]
            with open(file_path,'w') as csvfile:
                dict_writer = csv.DictWriter(csvfile,k)
                dict_writer.writeheader()
                dict_writer.writerows(x)
            return True
        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return False

    def read(self,id:int=0):
        pass