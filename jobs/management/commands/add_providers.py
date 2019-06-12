from django.core.management.base import BaseCommand
from django.conf import settings
import os,json
from jobs.handlers.postgres import PostgresDBHandler

postgres_db_handler=PostgresDBHandler()

class Command(BaseCommand):
    help = 'Add odds providers to DB'

    def handle(self, *args, **kwargs):
        # try:
        sql='''
        INSERT INTO providers(name,created_at,inserted_at,meta)
        VALUES(%s,now(),now(),%s)
        ON CONFLICT(name)
        DO NOTHING
        '''
        providers=[]
        with open(os.path.join(settings.BASE_DIR,"fixtures/providers_list.json")) as jfile:
            data=json.load(jfile)

        for v in data:
            providers.append((v["name"],'{}'))

        postgres_db_handler.insert_update_many(
            sql,providers
        )
        [self.stdout.write(self.style.SUCCESS("Created/Updated: {}".format(p["name"]))) for p in data]
        # except Exception as e:
        #     self.stdout.write(self.style.ERROR('Error:{}'.format(e)))