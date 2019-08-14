from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from jobs.models import AbstractModel

class Provider(AbstractModel):
    name=models.CharField(max_length=255, unique=True)
    hosts=ArrayField(
        models.CharField(max_length=255)
    )
    
    class Meta:
        db_table="providers"
        verbose_name_plural ="Providers"

    def __str__(self):
        return "provider_id:{}".format(self.id)