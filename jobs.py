from jobs.services import JobsService
from jobs.defaults import StorageHandler
from jobs.handlers.csv_storage_handler import CsvStorageHandler

provider_list = [
    "https://www.fuzu.com/categories/it-software",
    "https://www.brightermonday.co.ug/jobs/technology/",
    "https://www.brightermonday.co.ke/jobs/technology/",
    "https://www.brightermonday.co.tz/jobs/technology/",
    "https://www.careerpointkenya.co.ke/category/ict-jobs-in-kenya/",
    "https://www.pigiame.co.ke/it-telecoms-jobs",
    "https://jobwebkenya.com/job-category/ittelecom-jobs-in-kenya-2013/",
    "https://ihub.co.ke/jobs",
]

# jobs_service = JobsService()
# jobs = jobs_service.fetch_list(provider_list)

# for job_list in jobs:
#     print("Fetched %s jobs."%len(job_list))
#     StorageHandler().write(job_list)
#     print("Stored %s jobs."%len(job_list))

data=StorageHandler().fetch_all()

CsvStorageHandler().write(data)

