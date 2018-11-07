from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from configparser import ConfigParser
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = model.Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_database_uri(filename:str='database.ini', section:str='postgresql', *args, **kwargs) -> str:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename=os.path.join(BASE_DIR,filename)
    database_uri=os.environ.get('DATABASE_URI')
    DEFAULT_PORT="5432"
    if database_uri:
        return database_uri

    else:
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        database_uri="postgresql+psycopg2://{}:{}@{}:{}/{}".format(db["user"],
                                                db["password"],
                                                db["host"],
                                                DEFAULT_PORT,
                                                db["database"])
        return database_uri

SQLALCHEMY_DATABASE_URI=get_database_uri()

config.set_main_option('sqlalchemy.url',SQLALCHEMY_DATABASE_URI)

SQLALCHEMY_DATABASE_URI=""


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
