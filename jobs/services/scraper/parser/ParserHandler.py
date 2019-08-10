
import re
import sys
from typing import Dict,List
from jobs.services.scraper.parser.AbstractParserHandler import AbstractParserHandler
from jobs.handlers.error_handler import ErrorLogHandler

class ParserHandler(AbstractParserHandler,ErrorLogHandler):

    def __init__(self):
        self.NEW_KEYS:Dict={
            "job_techs":self.get_jobs_technologies,
            "months":self.get_months,
            "employment":self.get_employment_type
        }

    def parse_job(self,job:Dict,) -> Dict:
        try:
            for k,f in self.NEW_KEYS.items():
                job.update(f(job))
            return job
        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return job

    def parse_job_list(self,job_list:List[Dict]) -> List[Dict]:
        try:
            data=[]
            for job in job_list:
                job=self.parse_job(job)
                data.append(job)
            # data=list(map(self.parse_job,job_list))
            return data
        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return job_list


    def get_jobs_technologies(self,job:Dict) -> Dict:
        try:
            Languages = ['ActionScript', 'Ada', 'Arduino', 'Assembly', 'AutoIt', 'Awk', 'Bash', 'Visual Basic', 
            'C', 'C#', 'C/C++', 'C++', 'Css',"css3","Html","Html5", 'Caml', 'Clojure', 'COBOL', 'CoffeeScript', 'Dart', 'ECMAScript', 
            'Elixir', 'Erlang', 'Fortran', 'Go', 'Groovy', 'Haskell', 'Java', 'JavaScript', 'Julia', 'Kotlin',
             'Lisp', 'Lua', 'Maple', 'Mathematica', 'MATLAB', 'Mercury', 'Objective-C', 'OCaml', 'OpenCL', 
             'Pascal', 'Perl', 'PHP', 'SQL', 'PowerScript', 'PowerShell', 'Prolog', 'Puppet', 'Python', 'R',
              'Ruby', 'Rust', 'SAS', 'Scala', 'Scilab', 'SPARK', 'SPSS', 'TypeScript', 'VBScript','Visual Basic .NET', 'XQuery']
            
            # https://en.wikipedia.org/wiki/Comparison_of_web_frameworks#Python
            #  https://hotframeworks.com/
            frameworks=["Django","React","Angular","Vue","Flask","ASP.NET","Laravel","symfony",
            "wordpress","Drupal","Rails","Express","Node js"]            

            technologies=Languages+frameworks

            fields_=["description","skills","responsibilities","qualifications","instructions","education_requirements"]
            
            s=""
            for f in fields_:
                try:
                    v=job[f]
                    if v==None:continue
                    if type(v)==list:v=" ".join(v)
                    s+= " " + v
                except Exception as e:
                    print(e)
                    
            # s=' '.join(v or '' for k,v in job.items() if k in fields_)
            # s= ' '.join(job[i] for i in fields_ if type(job[i]))
            technologies = map(re.escape, technologies)
            technologies_regex = '(?<=[ ,(])('+'|'.join(technologies)+')(?=[,|\)])'
            techs = re.findall(technologies_regex, s, flags=re.IGNORECASE)
            # do something
            return {"technologies":[str(i).lower() for i in list(set(techs))]}

        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return {"technologies":[]}

    def get_months(self,job:Dict) -> Dict:
        # (\d)[\s.]?(years?|months?|weeks?)|none
        try:
            durations = {"year": 12, "month": 1, "week": 0.25}
            level_regex = r"(\d+)[\s.]?(year|month|week)s?|(none)"
            fields = ["experience_requirement"]
            string = ''.join(job.get(f,"") for f in fields if type(job.get(f,""))==str)
            match = re.search(level_regex, string)
            if match==None: return {"months":""}
            if match.group(3):
                return {"months":""}
            quantity = match.group(1)
            x = match.group(2)
            return  {"months":str(int(quantity)*durations[x])}
        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return  {"months":""}

    def get_employment_type(self,job:Dict) -> Dict:
        try:
            fields_=["job_title","employment_type","description","requirements","skills"]
            default = job.get("employment_type", "")
            s=''.join(str(v) or '' for k,v in job.items() if k in fields_ and v!=None)
            type_regex = r'(?:FULL|PART)[_\- ]?TIME'
            employment_type = re.findall(type_regex, s, flags=re.IGNORECASE) + default if type(default) is list else [default]
            # parse_job_list
            return  {"employment_type": employment_type[0]}
        except Exception as e:
            self.logError(sys.exc_info(), e, True)
            return  {"employment_type": ""}
            

