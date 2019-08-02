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

files=['fuzu.com.json', 'brightermonday.co.ke.json', 'pigiame.co.ke.json', 
    'brightermonday.co.tz.json', 'ihub.co.ke.json', 'brightermonday.co.ug.json']

def fixtures_to_db():
    from jobs.entities.JobListing import JobListing
    for i in files:
        with open(django.conf.settings.BASE_DIR+"/fixtures/"+i,"r") as jfile:
            d=json.load(jfile)
            for j in d:
                if type(j)==dict:
                    c=JobListing(meta=j)
                    c.save()

# def print_to_file(name):

def fixtures_to_csv():
    from jobs.handlers.csv_storage_handler import CsvStorageHandler
    from jobs.services.scraper.providers import providers
    csv_handler=CsvStorageHandler()
    parse_fixture = lambda x,y:providers[x].get_parser().parse_job_list(y)
    for f in files:
        path=django.conf.settings.BASE_DIR+"/fixtures/"+os.path.splitext(f)[0]+".csv"
        with open(django.conf.settings.BASE_DIR+"/fixtures/"+f,"r") as jfile:
            data=json.load(jfile)
            data=parse_fixture(os.path.splitext(f)[0],data)
            csv_handler.write(path,data)
    return True
            

fixtures_to_csv()

