
import dateutil.parser
from rest_framework import status
from rest_framework.exceptions import APIException
from jobs.models import JobListing,Provider,HiringOrganization
from jobs.handlers.postgres import PostgresDBHandler


class JobsApiSerializer:
    db_handler=PostgresDBHandler()
    def filter(self, filters):
        posted=dateutil.parser.parse(filters.get("posted")) if filters.get("posted",default=None) != None else None
        deadline=dateutil.parser.parse(filters.get("deadline")) if filters.get("deadline",default=None) != None else None
        job_title=filters.get("title",default=None)
        location=filters.get("location",default=None)
        company=filters.get("organisation",default=None)
        sortable_fields={'id':'job.id', 'title':'job.title', 'organisation':'hiring_organization.name',
                        'location':'job.location', 'type':'job.employment_type', 'posted':'job.dead_posted', 'deadline':'job.valid_to'}
        order_options={"asc":"ASC","desc":"DESC"}
        sortBy=filters.get("sortBy",default="id")
        orderBy=filters.get("order",default="asc")
        if sortBy not in list(sortable_fields.keys()):
            raise APIException("Invalid sortBy option")
        if orderBy not in list(order_options.keys()):
            raise APIException("Invalid order option")

        sql='''
        SELECT job.id as id, job.title as title, hiring_organization.name as organization, job.location as location, 
        job.employment_type as type, job.industry as industry, job.date_posted as posted, job.valid_to as deadline,
        job.url as url, job.months as months, job.skills as skills, job.tags as tags
        FROM job_listings job
        INNER JOIN hiring_organizations hiring_organization ON hiring_organization.id = job.hiring_organization_id
        '''
        params={}
        sql_filters=[]
        if posted !=None:
            sql_filters.append("date(job.date_posted) >= date(%(posted)s)")
            params["posted"]=posted.date().strftime("%Y-%m-%d")
        if deadline !=None:
            sql_filters.append("date(job.valid_to) >= date(%(deadline)s)")
            params["deadline"]=deadline.date().strftime("%Y-%m-%d")

        if company != None:
            sql_filters.append(" LOWER(hiring_organization.name) ~ LOWER(%(company)s)")
            params["company"]=company

        if job_title != None:
            sql_filters.append(" LOWER(job.title) ~ LOWER(%(job_title)s)")
            params["job_title"]=job_title

        if location != None:
            sql_filters.append(" LOWER(job.location) ~ LOWER(%(location)s)")
            params["location"]=location

        if len(sql_filters)>0:
            sql+=" WHERE " +" AND ".join(sql_filters)

        sql+=" ORDER BY {sort_field} {order}".format(sort_field=sortable_fields[sortBy], order=order_options[orderBy])
        data= self.db_handler.fetch_dict(sql,params,one=False)
        return data

        