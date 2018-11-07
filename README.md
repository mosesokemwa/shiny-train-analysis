# Jobs Scraper
## Description 
- This looks like a job for spiderman.

## setting up postgresql
- create a postgres database and add its `POSTGRES_DATABASE_URI` to path in the following format
```bash

```
- alternatively you can create a database.ini file in the folder `jobs/handlers/postgres`, this file will be ignored by git
```
[postgresql]
host=localhost
database=jobs
user=user
password=pass
```

#### Postgres database migrations
- We use alembic to make database migrations
```bash
cd jobs/handlers/postgres
alembic revision -m "message"
alembic upgrade head
```

## setting up mongodb
- Add `MONGO_DATABASE_URI` to path in the following format.
```bash

```
- alternatively you can create a `database.ini` file in the folder `jobs/handlers/mongodb`, this file will be ignored by git
```
[mongodb-atlas]
host=atlas
user=user
password=password

[mongodb-local]
host=host
user=user
port=27017
password=password
```