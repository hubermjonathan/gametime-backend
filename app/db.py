import psycopg2
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


def connect():
    connection = psycopg2.connect(
        host=environ.get('DB_URL'),
        database=environ.get('DB_NAME'),
        user=environ.get('DB_USERNAME'),
        password=environ.get('DB_PASSWORD')
    )
    connection.autocommit = True

    return connection


def drop_and_create_tables():
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(open('app/schema.sql', 'r').read())
        result = ('successfully dropped and created tables', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result


def create_user(name, email, phone_number):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (name, email, phone_number)
            VALUES (%s, %s, %s);
            """,
            (name, email, phone_number)
        )
        result = ('successfully created user', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result
