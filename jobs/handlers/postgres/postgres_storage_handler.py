import os
import abc
import datetime

from jobs.handlers.abstract_storage_handler import AbstractStorageInterface
from jobs.handlers.postgres.config import PostgresConfig
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



database_uri=PostgresConfig().get_database_uri()
engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)
Base = declarative_base() 

class PostgresStorageHandler(AbstractStorageInterface):
    def __init__(self,pg_conf=PostgresConfig(), *args, **kwargs):
        self.pg_conf=pg_conf
        # Session = sessionmaker(bind=engine)

    def read(self):
        pass

    def write(self):
        pass


