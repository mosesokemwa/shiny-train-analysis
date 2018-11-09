from typing import List,Dict
from pymongo import MongoClient
from jobs.handlers.abstract_storage_handler import AbstractStorageInterface
from jobs.handlers.mongodb.config import MongoConfig

class MongoDbStorageHandler(AbstractStorageInterface):

    def __init__(self, mongoconf=MongoConfig(), *args, **kwargs):
        self.mongo_config=mongoconf
        self.client=MongoClient(mongoconf.get_database_uri())
        self.database=self.client[mongoconf.DATABASE_NAME]

    def write(self,data:List[Dict]) -> bool:
        try:
            mongo_col=self.database[self.mongo_config.COLUMN]
            ids=mongo_col.insert_many(data)
            return True

        except Exception as e:
            print(e)
            return False

    def read(self) -> List[Dict]:
        pass

    def fetch_all(self) -> List[Dict]:
        try:
            return [x for x in self.database["jobs_records"].find()]
        except Exception as e:
            raise Exception("Execption {}".format(e))
