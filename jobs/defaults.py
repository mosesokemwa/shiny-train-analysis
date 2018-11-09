# from jobs.handlers.postgres import postgres_storage_handler
from jobs.handlers.mongodb import mongodb_storage_handler


StorageHandler = mongodb_storage_handler.MongoDbStorageHandler

providers_list = [
    "https://www.fuzu.com/categories/it-software",
    "https://www.brightermonday.co.ug/jobs/technology/",
    "https://www.brightermonday.co.ke/jobs/technology/",
    "https://www.brightermonday.co.tz/jobs/technology/",
    "https://www.pigiame.co.ke/it-telecoms-jobs",
    "https://ihub.co.ke/jobs",
    # "https://www.careerpointkenya.co.ke/category/ict-jobs-in-kenya/",
    # "https://jobwebkenya.com/job-category/ittelecom-jobs-in-kenya-2013/",
]
