# setup django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobs.settings')
import django
django.setup()


from jobs.services.scraper.scraper import Scraper

scraper=Scraper()


test_provider=list(scraper.provider_urls.values())[0]
data=scraper.fetch(test_provider)
x=scraper.parse(data[0],data[1])
scraper.store_to_json(data[2],x)
print(x)
