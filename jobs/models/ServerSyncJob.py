from django.db import models
from jobs.models import AbstractModel

class ServerSyncJob(AbstractModel):
    error = models.BooleanField( default= False)
    error_message = models.TextField(blank = True, null =  True)

    class Meta:
        db_table = "server_sync_jobs"