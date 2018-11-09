from jobs.services import JobsService
from jobs.defaults import StorageHandler
from jobs.handlers.cleaner_handler import CleanHtmlHandler
from jobs.handlers.csv_storage_handler import CsvStorageHandler
from jobs.parser.ParserHandler import ParserHandler

provider_list = [
    "https://www.fuzu.com/categories/it-software",
    "https://www.brightermonday.co.ug/jobs/technology/",
    "https://www.brightermonday.co.ke/jobs/technology/",
    "https://www.brightermonday.co.tz/jobs/technology/",
    "https://www.pigiame.co.ke/it-telecoms-jobs",
    "https://ihub.co.ke/jobs",
    # "https://www.careerpointkenya.co.ke/category/ict-jobs-in-kenya/",
    # "https://jobwebkenya.com/job-category/ittelecom-jobs-in-kenya-2013/",
]

jobs_service = JobsService()
jobs = jobs_service.fetch_list(provider_list)

cleaner=CleanHtmlHandler()
for job_list in jobs:
    print("Fetched %s jobs."%len(job_list))
    StorageHandler().write(cleaner.clean_data(job_list))
    print("Stored %s jobs."%len(job_list))

data=StorageHandler().fetch_all()
new_data=ParserHandler().parse_job_list(data)
CsvStorageHandler().write(new_data)
