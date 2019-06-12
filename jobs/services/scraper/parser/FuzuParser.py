from typing import List,Dict

from jobs.services.scraper.parser.ParserHandler import ParserHandler

class FuzuJobsParser(ParserHandler):

    def parse_job(self,job: Dict) -> Dict:
        return ParserHandler.parse_job(self,job)

    def parse_job_list(self,job_list: List[Dict]) -> List[Dict]:
        return ParserHandler.parse_job_list(self,job_list)
