from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class JobListing(models.Model):
    name=models.CharField(max_length=255, unique=True)
    company=models.ForeignKey('jobs.Company',related_name="company_jobs", on_delete=models.SET_NULL,null=True)
    provider=models.ForeignKey('jobs.Providers',related_name="provder_jobs", on_delete=models.SET_NULL,null=True)
    description=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    inserted_at = models.DateTimeField(auto_now=True)
    meta = JSONField(blank=True, default=dict)

    class Meta:
        db_table="job_listings"
        verbose_name_plural ="JobListings"
    def __str__(self):
        return "job_listing:{}".format(self.id)