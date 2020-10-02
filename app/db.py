'''
functions:
    create_user(name, email, phone_number)
        creates a user
    add_phone_number(user_id, phone_number)
        adds a new phone number to a user
    remove_phone_number(user_id, phone_number)
        removes an extra phone number from a user
    create_team(name, user_id)
        creates a team, adds the coach, and creates the default group
    join_team(user_id, team_id)
        adds a user to a team and its default group
    change_permission_level(user_id, team_id, privelege_level)
        changes the permission level for a user on a team
    leave_team(user_id, team_id)
        removes a user from a team and any groups from that team

TODO:
    functions:
        general get functions
        get teams for a user
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


def drop_test_tables():
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(open('app/schemas/test_schema.sql', 'r').read())
        result = ('successfully dropped and created tables', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result


def drop_prod_tables():
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(open('app/schemas/prod_schema.sql', 'r').read())
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


def create_team(name, user_id):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            DO $$
            DECLARE new_team_id integer;
            BEGIN
                INSERT INTO teams (name, fund_goal, fund_current, fund_desc, account_number, routing_number, owner)
                VALUES (%s, 0, 0, '', 0, 0, %s)
                RETURNING team_id INTO new_team_id;

                INSERT INTO usersteams (user_id, team_id, privelege_level, fund_goal, fund_current, fund_desc)
                VALUES (%s, new_team_id, 0, 0, 0, '');

                INSERT INTO groups (team_id, name)
                VALUES (new_team_id, 'All Members');
            END $$
            ''',
            (name, user_id, user_id)
        )

        result = ('successfully created team', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result


def join_team(user_id, team_id):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO usersteams (user_id, team_id, privelege_level, fund_goal, fund_current, fund_desc)
            VALUES (%s, %s, 0, 0, 0, '');

            INSERT INTO usersgroups (user_id, group_id)
            VALUES (%s, (
                SELECT group_id
                FROM groups
                WHERE team_id=%s AND name='All Members'
            ));
            ''',
            (user_id, team_id, user_id, team_id)
        )

        result = ('successfully joined team', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result


def change_permission_level(user_id, team_id, privelege_level):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            UPDATE usersteams
            SET privelege_level=%s
            WHERE user_id=%s AND team_id=%s;
            ''',
            (privelege_level, user_id, team_id)
        )
        result = ('successfully changed permission level', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    connection.close()
    return result


def leave_team(user_id, team_id):
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute(
            '''
            DELETE FROM usersteams
            WHERE user_id=%s AND team_id=%s;
            ''',
            (user_id, team_id)
        )

        cursor.execute(
            '''
            SELECT group_id
            FROM groups
            WHERE team_id=%s;
            ''',
            (team_id,)
        )

        for row in cursor:
            cursor2 = connection.cursor()
            cursor2.execute(
                '''
                DELETE FROM usersgroups
                WHERE user_id=%s AND group_id=%s;
                ''',
                (user_id, row[0])
            )

        result = ('successfully left team', 200)
    except Exception as e:
        result = (str(e), 500)

    cursor.close()
    cursor2.close()
    connection.close()
    return result
