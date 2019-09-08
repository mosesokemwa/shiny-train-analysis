
import dateutil.parser
import itertools
from rest_framework import status
from rest_framework.exceptions import APIException
from jobs.models import JobListing,Provider,HiringOrganization
from jobs.handlers.postgres import PostgresDBHandler

class JobLocationsSerializer:
    db_handler=PostgresDBHandler()
    def get(self,filters):
        location_type = filters.get("type","cities")
        location_fields = {"cities":"job.city","countries":"job.country"}
        if location_type not in location_fields.keys():
            return []
        sql='''
        SELECT array_agg(DISTINCT LOWER({field}) ) as locations FROM job_listings job
        '''.format(field=location_fields[location_type])
        data = self.db_handler.fetch_dict(sql,{},one=True)
        if data:
            bad_data = [None,""]
            [data[0]["locations"].remove(i) for i in bad_data if i in data[0]["locations"]]
            return {"locations":data[0]["locations"]}
        return {"locations":[]}


class SyncJobsSerializer:
    db_handler=PostgresDBHandler()
    def get(self,filters):
        latest = filters.get("latest",None)
        sql='''
        SELECT s.id as id, s.error as error, s.error_message as error_message, s.created_at as created_at
        FROM server_sync_jobs s
        ORDER BY s.created_at DESC
        '''
        sql += ' LIMIT 1' if type(latest) == str  and latest.lower() == "true" else ""
        print(sql)
        data =  self.db_handler.fetch_dict(sql,{},one=False)
        return data

class ProvidersSerializer:
    db_handler=PostgresDBHandler()
    def get(self,filters):
        sql='''
        select provider.id as id, provider.name as name, provider.hosts as hosts, COUNT(job.id) as job_count, provider.created_at as created_at
        FROM providers provider 
        INNER JOIN job_listings job ON provider.id = job.provider_id
        GROUP BY provider.id
        ORDER BY provider.id
        ''';
        data =  self.db_handler.fetch_dict(sql,{},one=False)
        return data

class TechnologiesSerializer:
    db_handler=PostgresDBHandler()
    def get(self):
        sql='SELECT  DISTINCT UNNEST(job.technologies) FROM job_listings job'
        data= self.db_handler.fetch(sql,{},one=False)
        return list(itertools.chain.from_iterable(data))

class JobsApiSerializer:
    db_handler=PostgresDBHandler()
    def filter(self, filters):
        posted=dateutil.parser.parse(filters.get("posted")) if filters.get("posted",default=None) != None else None
        deadline=dateutil.parser.parse(filters.get("deadline")) if filters.get("deadline",default=None) != None else None
        deadline_blank=filters.get("deadlineBlank",default=None)
        job_title=filters.get("title",default=None)
        cities=filters.getlist("cities[]",default=None)
        organization=filters.get("organization",default=None)
        technologies=filters.getlist("tags[]",default=None)
        provider_id = filters.get("provider_id",default=None)
        page_size = int(filters.get("page_size", default=100))
        page = int(filters.get("page", default=1))
        sortable_fields={'id':'job.id', 'title':'job.title', 'organization':'hiring_organization.name',
                        'cities':'job.city', 'type':'job.employment_type', 'posted':'job.date_posted', 'deadline':'job.valid_to'}
        order_options={"asc":"ASC","desc":"DESC"}
        sortBy=filters.get("sortBy",default="id")
        orderBy=filters.get("order",default="asc")
        if sortBy not in list(sortable_fields.keys()):
            raise APIException("Invalid sortBy option")
        if orderBy not in list(order_options.keys()):
            raise APIException("Invalid order option")

        sql='''
        SELECT job.id as id, job.title as title, hiring_organization.name as organization, job.city as city, job.country as country,
        job.employment_type as type, job.industry as industry, job.date_posted as posted, job.valid_to as deadline,
        job.url as url, job.months as months, job.skills as skills, job.technologies as technologies,
        job.provider_id as provider_id, job.created_at as created_at, job.inserted_at as updated_at
        FROM job_listings job
        INNER JOIN hiring_organizations hiring_organization ON hiring_organization.id = job.hiring_organization_id
        '''
        count_sql='''
        SELECT COUNT(job.id) FROM job_listings job
        INNER JOIN hiring_organizations hiring_organization ON hiring_organization.id = job.hiring_organization_id
        '''
        count_params={}

        if provider_id !=None:
            count_sql +=' WHERE job.provider_id= %(provider_id)s'
            count_params.update({"provider_id":provider_id})

        count=self.db_handler.fetch(count_sql,count_params,one=True)
        if count and len(count)==1:
            count=count[0]
        params={}
        sql_filters=[]
        if posted !=None:
            sql_filters.append("date(job.date_posted) >= date(%(posted)s)")
            params["posted"]=posted.date().strftime("%Y-%m-%d")
        if deadline !=None:
            deadline_filter = "date(job.valid_to) >= date(%(deadline)s)"
            if deadline_blank !=None:
                deadline_filter = f" ( {deadline_filter} OR job.valid_to is null )"
            sql_filters.append(deadline_filter)
            params["deadline"]=deadline.date().strftime("%Y-%m-%d")

        if organization != None:
            sql_filters.append(" LOWER(hiring_organization.name) ~ LOWER(%(company)s)")
            params["company"]=organization

        if job_title != None:
            sql_filters.append(" LOWER(job.title) ~ LOWER(%(job_title)s)")
            params["job_title"]=job_title
        
        if provider_id != None:
            sql_filters.append(" job.provider_id = %(provider_id)s")
            params["provider_id"] = provider_id

        if technologies != None and len(technologies)>0:
            tech_filters=[]
            # @todo find a better method
            for i,tech in enumerate(technologies):
                if type(tech)==str and tech !="":
                    # tech_filters.append(" job.technologies @> %("+"tech"+str(i)+")s::VARCHAR[255]")
                    # params["tech"+str(i)]=[tech.lower()]
                    tech_filters.append("%("+"tech"+str(i)+")s::VARCHAR = ANY(job.technologies)")
                    params["tech"+str(i)]=tech.lower()
                    
            tech_sql=" OR ".join(tech_filters)
            sql_filters.append("({tech_sql})".format(tech_sql=tech_sql))

        if cities != None and len(cities)>0:
            city_filters=[]
            # @todo find a better method
            for i,city in enumerate(cities):
                if type(city)==str and city !="":
                    city_filters.append(" LOWER(job.city) ~ LOWER(%(city"+str(i)+")s)")
                    params["city"+str(i)]=city
            sql_filters.append(" OR ".join(city_filters))

        if len(sql_filters)>0:
            sql+=" WHERE " +" AND ".join([i for i in sql_filters if type(i)==str and i!=""])
        sql+=" ORDER BY {sort_field} {order}".format(sort_field=sortable_fields[sortBy], order=order_options[orderBy])
        sql += " LIMIT {page_size} OFFSET {offset}".format(page_size=page_size, offset=(page-1)*page_size)
        # print(sql%params)
        data= self.db_handler.fetch_dict(sql,params,one=False)
        return {"data":data,"count":count,"page":page}


