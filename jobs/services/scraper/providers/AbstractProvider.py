import abc

class AbstractProvider(abc.ABC):
    
    def get_parser(self):
        return False