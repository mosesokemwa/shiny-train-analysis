import os
import abc
from configparser import ConfigParser

from jobs import settings

class AbstractMongoConfig(abc.ABC):
    
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_database_uri(self,*args, **kwargs) -> str:
        pass



class MongoConfig(AbstractMongoConfig):

    DATABASE_NAME="jobs"

    def __init__(self, *args, **kwargs):
        pass

    def get_database_uri(self,filename:str='database.ini', section:str='mongodb-local', *args, **kwargs) -> str:
        # mongodb://10.10.10.179:27017/
        filename=os.path.join(settings.BASE_DIR, "jobs/handlers/mongodb/"+filename)
        database_uri=os.environ.get('MONGO_DATABASE_URI')
        if database_uri:
            return database_uri
        else:
            parser = ConfigParser()
            parser.read(filename)
            db = {}
            if parser.has_section(section):
                params = parser.items(section)
                for param in params:
                    db[param[0]] = param[1]
            
            else:
                raise Exception('Section {0} not found in the {1} file'.format(section, filename))
            if section=="mongodb-local":
                database_uri="mongodb://{}:{}@{}:{}".format(db["user"],
                                                        db["password"],
                                                        db["host"],
                                                        db["port"],)
            elif section=="mongodb-atlas":
                database_uri="mongodb+srv://{}:{}@{}/{}?retryWrites=true".format(db["user"],
                                                                                db["password"],
                                                                                db["host"],
                                                                                self.DATABASE_NAME)
                                                                            
            return database_uri