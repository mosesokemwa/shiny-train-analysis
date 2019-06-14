# setup django
import os,json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobs.settings')
import django
django.setup()


# from jobs.services.scraper.scraper import Scraper


# scraper=Scraper()


# test_provider=list(scraper.provider_urls.values())[0]
# data=scraper.fetch(test_provider)
# x=scraper.parse(data[0],data[1])
# scraper.store_to_json(data[2],x)
# print(x)

def fixtures_to_db():
    data=['fuzu.json', 'brightermonday.co.ke.json', 'pigiame.co.ke.json', 
    'brightermonday.co.tz.json', 'ihub.co.ke.json', 'brightermonday.co.ug.json']
    from jobs.entities.JobListing import JobListing

    for i in data:
        with open(django.conf.settings.BASE_DIR+"/fixtures/"+i,"r") as jfile:
            d=json.load(jfile)
            for j in d:
                if type(j)==dict:
                    c=JobListing(meta=j)
                    c.save()

# def print_to_file(name):

