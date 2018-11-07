import abc
from typing import List



class AbstractStorageInterface(abc.ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def write(self,data:List) -> bool:
        pass

    @abc.abstractmethod
    def read(self,id:int=0):
        pass