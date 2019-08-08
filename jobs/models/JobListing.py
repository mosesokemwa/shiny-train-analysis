from django.db import models
from django.contrib.postgres.fields import ArrayField

class JobListing(models.Model):

    title=models.CharField(max_length=255,null=False)
    hiring_organization=models.ForeignKey('jobs.HiringOrganization',related_name="organization_jobs", on_delete=models.CASCADE,null=False)
    provider=models.ForeignKey('jobs.Provider',related_name="provder_jobs", on_delete=models.CASCADE,null=False)
    
    # skills
    skills=ArrayField(
        models.CharField(max_length=255)
    )
    # tags
    tags=ArrayField(
        models.CharField(max_length=255)
    )

    # FULL/PART TIME
    employment_type=models.CharField(max_length=255,null=True)

    # validity
    date_posted= models.DateField(null=True)
    valid_to=models.DateField(null=True)

    #url to job
    url=models.TextField(null=False)
    #months -> experience in months
    months=models.PositiveIntegerField()
    # name of industry
    industry=models.CharField(max_length=255)

    # description / responsibilities / education / experience / qualifications
    description=models.TextField(null=True)
    education_requirements=models.TextField(null=True)
    qualifications=models.TextField(null=True)
    responsibilities=models.TextField(null=True)
    instructions=models.TextField(null=True)
    
    def __str__(self):
        return "job_listing:{}".format(self.id)

    class Meta:
        db_table="job_listings"
        verbose_name_plural ="JobListings"