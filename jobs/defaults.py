# from jobs.handlers.postgres import postgres_storage_handler
from jobs.handlers.mongodb import mongodb_storage_handler


StorageHandler = mongodb_storage_handler.MongoDbStorageHandler
