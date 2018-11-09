from jobs.parser.AbstractParserHandler import AbstractParserHandler
from typing import Dict,List
import re

class ParserHandler(AbstractParserHandler):

    def __init__(self):
        self.NEW_KEYS:Dict={
            "job_tags":self.get_jobs_tag,
            "months":self.get_months,
            "employment":self.get_employment_type
        }

    def parse_job(self,job:Dict,) -> Dict:
        for k,f in self.NEW_KEYS.items():
            job.update(f(job))
        return job

    def parse_job_list(self,job_list:List[Dict]) -> List[Dict]:
        return list(map(self.parse_job,job_list))

    def get_jobs_tag(self,job:Dict) -> Dict:
        Languages = ['4th Dimension', '4D', 'ABAP', 'ABC', 'ActionScript', 'Ada', 'Agilent VEE', 'Algol', 'Alice', 'Angelscript', 'Apex', 'APL', 'AppleScript', 'Arc', 'Arduino', 'ASP', 'AspectJ', 'Assembly', 'ATLAS', 'Augeas', 'AutoHotkey', 'AutoIt', 'AutoLISP', 'Automator', 'Avenue', 'Awk', 'Bash', '(Visual) Basic', 'bc', 'BCPL', 'BETA', 'BlitzMax', 'Boo', 'Bourne Shell', 'Bro', 'C', 'C Shell', 'C#', 'C++','CLI', 'C-Omega', 'Caml', 'Ceylon', 'CFML', 'cg', 'Ch', 'CHILL', 'CIL', 'CL (OS/400)', 'Clarion', 'Clean', 'Clipper', 'Clojure', 'CLU', 'COBOL', 'Cobra', 'CoffeeScript', 'ColdFusion', 'COMAL', 'Common Lisp', 'Coq', 'cT', 'Curl', 'D', 'Dart', 'DCL', 'DCPU-16 ASM', 'Delphi', 'Object Pascal', 'DiBOL', 'Dylan', 'E', 'eC', 'Ecl', 'ECMAScript', 'EGL', 'Eiffel', 'Elixir', 'Emacs Lisp', 'Erlang', 'Etoys', 'Euphoria', 'EXEC', 'F#', 'Factor', 'Falcon', 'Fancy', 'Fantom', 'Felix', 'Forth', 'Fortran', 'Fortress', '(Visual) FoxPro', 'Gambas', 'GNU Octave', 'Go', 'Google AppsScript', 'Gosu', 'Groovy', 'Haskell', 'haXe', 'Heron', 'HPL', 'HyperTalk', 'Icon', 'IDL', 'Inform', 'Informix-4GL', 'INTERCAL', 'Io', 'Ioke', 'J', 'J#', 'JADE', 'Java', 'Java FX Script', 'JavaScript', 'JScript', 'JScript.NET', 'Julia', 'Korn Shell', 'Kotlin', 'LabVIEW', 'Ladder Logic', 'Lasso', 'Limbo', 'Lingo', 'Lisp', 'Logo', 'Logtalk', 'LotusScript', 'LPC', 'Lua', 'Lustre', 'M4', 'MAD', 'Magic', 'Magik', 'Malbolge', 'MANTIS', 'Maple', 'Mathematica', 'MATLAB', 'Max', 'MSP', 'MAXScript', 'MEL', 'Mercury', 'Mirah', 'Miva', 'ML', 'Monkey', 'Modula-2', 'Modula-3', 'MOO', 'Moto', 'MS-DOS Batch', 'MUMPS', 'NATURAL', 'Nemerle', 'Nimrod', 'NQC', 'NSIS', 'Nu', 'NXT-G', 'Oberon', 'Object Rexx', 'Objective-C', 'Objective-J', 'OCaml', 'Occam', 'ooc', 'Opa', 'OpenCL', 'OpenEdge ABL', 'OPL', 'Oz', 'Paradox', 'Parrot', 'Pascal', 'Perl', 'PHP', 'Pike', 'PILOT', 'PL', 'I', 'PL', 'SQL', 'Pliant', 'PostScript', 'POV-Ray', 'PowerBasic', 'PowerScript', 'PowerShell', 'Processing', 'Prolog', 'Puppet', 'Pure Data', 'Python', 'Q', 'R', 'Racket', 'REALBasic', 'REBOL', 'Revolution', 'REXX', 'RPG (OS/400)', 'Ruby', 'Rust', 'S', 'S-PLUS', 'SAS', 'Sather', 'Scala', 'Scheme', 'Scilab', 'Scratch', 'sed', 'Seed7', 'Self', 'Shell', 'SIGNAL', 'Simula', 'Simulink', 'Slate', 'Smalltalk', 'Smarty', 'SPARK', 'SPSS', 'SQR', 'Squeak', 'Squirrel', 'Standard ML', 'Suneido', 'SuperCollider', 'TACL', 'Tcl', 'Tex', 'thinBasic', 'TOM', 'Transact-SQL', 'Turing', 'TypeScript', 'Vala', 'Genie', 'VBScript', 'Verilog', 'VHDL', 'VimL', 'Visual Basic .NET', 'WebDNA', 'Whitespace', 'X10', 'xBase', 'XBase++', 'Xen', 'XPL', 'XSLT', 'XQuery', 'yacc', 'Yorick', 'Z shell']

        fields_=["description","skills","responsibilities"]
        s=''.join(v or '' for k,v in job.items() if k in fields_)
        Languages = map(re.escape, Languages)
        skills_regex = '(?<=[ ,(])('+'|'.join(Languages)+')(?=[,|\)])'
        skills = re.findall(skills_regex, s, flags=re.IGNORECASE)
        print(skills)
        # do something
        return {"tags":','.join(skills)}

    def get_months(self,job:Dict) -> Dict:
        # (\d)[\s.]?(years?|months?|weeks?)|none
        durations = {"year": 12, "month": 1, "week": 0.25}
        level_regex = r"(\d+)[\s.]?(year|month|week)s?|(none)"
        fields = ["experience_requirement"]
        string = ''.join(job.get(f,"") for f in fields)
        match = re.search(level_regex, string)
        if match.group(3) == "none":
            return {"months":"0"}
        quantity = match.group(1)
        x = match.group(2)
        return  {"months":str(int(quantity)*durations[x])}

    def get_employment_type(self,job:Dict) -> Dict:
        fields_=["job_title","employment_type","description","requirements","skills"]
        default = job.get("employment_type", "")
        s=''.join(str(v) or '' for k,v in job.items() if k in fields_)
        type_regex = r'(?:FULL|PART)[_\- ]?TIME'
        employment_type = re.findall(type_regex, s, flags=re.IGNORECASE) + default if type(default) is list else [default]
        # parse_job_list
        return  {"employment_type": employment_type[0]}

# recieve a list of dicts/jobs field, keys to append
#  return a list of dicts/jobs with new fields i.e level, job StorageHandler
