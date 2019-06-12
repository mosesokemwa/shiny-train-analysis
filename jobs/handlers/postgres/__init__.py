from django.db import connection
import psycopg2.extras

class PostgresDBHandler:

    def __init__(self, *args, **kwargs):
        pass


    def fetch_dict(self,sql,params,one=True):
        data=None
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(
                sql,
                params
                )
            if one:
                data=cursor.fetchone()
            else:
                data=cursor.fetchall()
        return data

    def fetch(self,sql,params,one=True):
        data=None
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                params
                )
            if one:
                data=cursor.fetchone()
            else:
                data=cursor.fetchall()
        return data

    def insert_update_many(self,sql,data,many=True):
        with connection.cursor() as cursor:
            if many:
                psycopg2.extras.execute_batch(
                    cursor,
                    sql,
                    data
                )
            else:
                cursor.execute(
                    sql,
                    data
                )
        return True

    def execute_sql(self,sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
