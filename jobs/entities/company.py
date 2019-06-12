from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Company(models.Model):
    name=models.CharField(max_length=255, unique=True)
    description=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    inserted_at = models.DateTimeField(auto_now=True)
    meta = JSONField(blank=True, default=dict)

    class Meta:
        db_table="companies"
        verbose_name_plural ="Companies"
    def __str__(self):
        return "company:{}".format(self.name if self.name else self.id)