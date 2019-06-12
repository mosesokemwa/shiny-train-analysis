import abc
from typing import List,Dict
class AbstractParserHandler(abc.ABC):
    @abc.abstractmethod
    def parse_job(job: Dict) -> Dict:
        pass
    @abc.abstractmethod
    def parse_job_list(job_list: List[Dict]) -> List[Dict]:
        pass
