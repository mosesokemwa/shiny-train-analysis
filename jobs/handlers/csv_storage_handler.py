import csv 
import os
from typing import List,Dict
from jobs.handlers.abstract_storage_handler import AbstractStorageInterface
from jobs import settings


class CsvConfig:
    pass

class CsvStorageHandler(AbstractStorageInterface):
    
    def __init__(self, *args, **kwargs):
        pass

    def write(self,data:List[Dict]) -> bool:
        try:
            file_path = os.path.join(settings.BASE_DIR,"jobs.csv")
            k=data[0].keys()
            with open(file_path,'w') as csvfile:
                dict_writer = csv.DictWriter(csvfile,k)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            return True
        except Exception as e:
            raise Exception("{}".format(e))

    def read(self,id:int=0):
        pass