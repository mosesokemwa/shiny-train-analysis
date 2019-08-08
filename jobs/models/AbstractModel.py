from django.db import models
from django.contrib.postgres.fields import JSONField

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    inserted_at = models.DateTimeField(auto_now=True)
    meta = JSONField(null=True,default=dict)
    
    class Meta:
        abstract = True