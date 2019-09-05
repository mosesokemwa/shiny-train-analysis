import os, csv, abc, json
import dateutil.parser
from urllib.parse import urlparse

from jobs.services.scraper.providers import providers
from jobs import settings
from jobs.models import JobListing,HiringOrganization,Provider

class AbstractScraperStorageHandler(abc.ABC):

    @abc.abstractmethod
    def store(self,results)->bool:
        pass


class PostgresScraperStorageHandler(AbstractScraperStorageHandler):

    def store(self,results)->bool:
        provider_name = provider_name = providers[results[0]].name if hasattr(providers[results[0]],"name") else providers[results[0]].__class__.__name__
        provider=Provider.objects.get(name=provider_name)
        for job in results[1]:
            try:
                hiring_organization = HiringOrganization.objects.get(name=job["hiring_organization"])
            except HiringOrganization.DoesNotExist:
                hiring_organization=HiringOrganization(name=job["hiring_organization"])
                hiring_organization.save()
            except Exception as e:
                hiring_organization=None

            job_dict=dict(
                title=job["job_title"],
                provider=provider,
                hiring_organization=hiring_organization,
                country = job["country"] if type(job["country"])==str else "",
                city = job["city"] if type(job["city"])==str else "",
                # location=job["city"] if type(job["city"])==str else "" + " " + job["country"] if type(job["country"])==str else "",
                skills= [i for i in job["skills"].split("\n") if i != "" and type(i) == str ] if job["skills"] != None else None,
                technologies=[i for i in job["technologies"] if type(i)==str and i !=""] if job["technologies"] != None else None,
                employment_type=job["employment_type"],
                date_posted=dateutil.parser.parse(job["date_posted"]),
                valid_to=dateutil.parser.parse(job["valid_through"]) if job["valid_through"] is not None else None,
                url=job["url"],
                industry=job["industry"] if type(job["industry"]) == str else None,
                description=job["description"] if type(job["description"]) == str else "",
                education_requirements=job["education_requirements"] if type(job["education_requirements"]) == str else "",
                qualifications=job["qualifications"] if type(job["qualifications"]) == str else "",
                responsibilities=job["responsibilities"] if type(job["responsibilities"]) == str else "",
                instructions=job["instructions"] if type(job["instructions"]) == str else "",
            )

            try:
                job_=JobListing.objects.get(url=job["url"])
                for attr,value in job_dict.items():
                    setattr(job_,attr,value)
                job_.save()

            except JobListing.DoesNotExist:
                job_=JobListing(**job_dict)
                job_.save()
                
            except Exception as e:
                print(e)
        return True


class JsonScraperStorageHandler(AbstractScraperStorageHandler):

    def store(self,results)->bool:
        name=urlparse(results[2]).netloc.replace("www.","")
        with open(settings.BASE_DIR+"/fixtures/{}.json".format(name),"w") as infile:
            json.dump(results[1],infile)
        return True


class CsvScraperStorageHandler(AbstractScraperStorageHandler):

    def __init__(self, *args, **kwargs):
        self.FIELDS=["id","job_title","city","hiring_organization","employment_type",
        "months","date_posted","valid_through","technologies","source", "url"]


    def store(self,results) -> bool:
        url=results[2]
        name=urlparse(url).netloc.replace(".com","").replace("www.","")
        file_path=settings.BASE_DIR+"/fixtures/{}.csv".format(name)
        try:
            k=[i for i in results[1][0].keys() if i in self.FIELDS]
            x = [{f:v for f,v in element.items() if f in k} for element in results[1]]
            with open(file_path,'w') as csvfile:
                dict_writer = csv.DictWriter(csvfile,k)
                dict_writer.writeheader()
                dict_writer.writerows(x)
            return True
        except Exception as e:
            print(e)
            return False
