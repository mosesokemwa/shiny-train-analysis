from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Providers(models.Model):
    name=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    inserted_at = models.DateTimeField(auto_now=True)
    meta = JSONField(blank=True, default=dict)

    class Meta:
        db_table="providers"
        verbose_name_plural ="Providers"

    def __str__(self):
        return "provider_id:{}".format(self.id)