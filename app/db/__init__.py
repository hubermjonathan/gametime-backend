from . import groups
from . import messages
from . import schema
from . import teams
from . import users
import psycopg2
import psycopg2.pool
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))

connection_pool = psycopg2.pool.ThreadedConnectionPool(
    5,
    20,
    user=environ.get('DB_USERNAME'),
    password=environ.get('DB_PASSWORD'),
    host=environ.get('DB_URL'),
    port='5432',
    database=environ.get('DB_NAME')
)


def connect():
    connection = connection_pool.getconn()
    connection.autocommit = True
    return connection, connection_pool
