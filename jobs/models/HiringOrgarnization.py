from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

from jobs.models.AbstractModel import AbstractModel

class HiringOrganization(AbstractModel):
    name=models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True)

    class Meta:
        db_table="hiring_organizations"
        verbose_name_plural ="Hiring_Organizations"

    def __str__(self):
        return "organization:{}".format(self.name if self.name else self.id)