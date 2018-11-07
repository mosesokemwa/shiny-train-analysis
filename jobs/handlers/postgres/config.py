import os
import abc
from configparser import ConfigParser

from jobs import settings

class AbstractPostgresConfig(abc.ABC):
    
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_database_uri(self,*args, **kwargs) -> str:
        pass



class PostgresConfig(AbstractPostgresConfig):

    def __init__(self, *args, **kwargs):
        self.DEFAULT_PORT="5432"

    def get_database_uri(self,filename:str='database.ini', section:str='postgresql', *args, **kwargs) -> str:
        filename=os.path.join(settings.BASE_DIR, "jobs/handlers/postgres/"+filename)
        database_uri=os.environ.get('DATABASE_URI')
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
            database_uri="postgresql+psycopg2://{}:{}@{}:{}/{}".format(db["user"],
                                                    db["password"],
                                                    db["host"],
                                                    self.DEFAULT_PORT,
                                                    db["database"])
            return database_uri