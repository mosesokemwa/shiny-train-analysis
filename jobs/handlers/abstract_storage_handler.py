import abc
from typing import List,Dict


class AbstractStorageInterface(abc.ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def write(self,data:List[Dict]) -> bool:
        pass

    @abc.abstractmethod
    def read(self,id:int=0):
        pass