from jobs.services import JobsService
from jobs.defaults import StorageHandler

# provider_list = [
#     'https://www.brightermonday.co.ke/jobs/it-telecoms/eldoret',
#     'https://ihub.co.ke/jobs',
#     'https://www.fuzu.com/jobs/search'
# ]

provider_list = [
    "https://ihub.co.ke/jobs",
]


jobs_service = JobsService()
# jobs = jobs_service.fetch_list(provider_list)
# print(jobs)

# StorageHandler().write(data)
