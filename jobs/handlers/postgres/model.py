import datetime
from configparser import ConfigParser

from sqlalchemy import  DateTime, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

class Jobs(Base):
    __tablename__="jobs"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    job_title= Column(String)
    hiring_organization= Column(String)
    city= Column(String)
    country= Column(String)
    employment_type= Column(String)
    education_requirements= Column(String)
    qualifications= Column(String)
    experience_requirement=Column(Integer)
    industry= Column(String)
    date_posted =Column(DateTime)
    valid_through =Column(DateTime)
    description= Column(String)
    skills= Column(String)
    responsibilities= Column(String)
    value_currency = Column(String)
    min_value=Column(Integer)
    max_value= Column(Integer)
    value_period= Column(String)
    instructions= Column(String)

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return "{} {}".format(self.job_title,self.hiring_organization)

    def __repr__(self):
        return "{} {}".format(self.job_title,self.hiring_organization)
