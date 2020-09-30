'''
functions:
    create_user(name, email, phone_number) - creates a user
    add_phone_number(user_id, phone_number) - adds a new phone number to a user

TODO:
    functions:
        general get functions
        remove phone numbers
        management of permission levels
        join team
        leave team
        get teams for a user
        create team
        edit team
        remove member from team
        get members from team
        create group
        add player to group
        remove player from group

    unit test:
        give admin priv
        remove admin priv
        join team
        leave team
        view teams
        create team
        edit team
        view an manage team
'''


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
            '''
            INSERT INTO users (name, email, phone_number)
            VALUES (%s, %s, %s);
            ''',
            (name, email, phone_number)
        )
        result = ('successfully created user', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result


def add_phone_number(user_id, phone_number):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO phones (user_id, phone_number)
            VALUES (%s, %s);
            ''',
            (user_id, phone_number)
        )
        result = ('successfully added phone number', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result


def remove_phone_number(user_id, phone_number):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            DELETE FROM phones
            WHERE user_id=%s AND phone_number=%s;
            ''',
            (user_id, phone_number)
        )
        result = ('successfully removed phone number', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result
