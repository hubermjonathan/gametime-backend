from ..db.connection_manager import connection_manager


def create_user(first_name, last_name, email, phone_number):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO users (first_name, last_name, email, phone_number)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id;
            ''',
            (first_name, last_name, email, phone_number)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created user', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_user_id(email):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT user_id
            FROM users
            WHERE email=%s
            ORDER BY user_id
            DESC
            LIMIT 1;
            ''',
            (email,)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved user id', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def check_if_user_has_phone_number(user_id, phone_number):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT COUNT(*) as exists
            FROM phones
            WHERE user_id=%s AND phone_number=%s;
            ''',
            (user_id, phone_number)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully checked users phone numbers', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def add_phone_number_to_user(phone_number, user_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO phones (user_id, phone_number)
            VALUES (%s, %s);
            ''',
            (user_id, phone_number)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully added phone number to user', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_phone_number_from_user(phone_number, user_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            DELETE FROM phones
            WHERE user_id=%s AND phone_number=%s;
            ''',
            (user_id, phone_number)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed phone number from user', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_user(user_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM users
            WHERE user_id=%s;
            ''',
            (user_id,)
        )
        user_info = connection_manager.get_data(cursor)

        cursor.execute(
            '''
            SELECT phone_number
            FROM phones
            WHERE user_id=%s;
            ''',
            (user_id,)
        )
        phone_numbers = connection_manager.get_data(
            cursor, 'extra_phone_numbers')

        cursor.execute(
            '''
            SELECT teams.team_id, teams.name, usersteams.permission_level
            FROM teams
            INNER JOIN usersteams
            USING (team_id)
            WHERE user_id=%s;
            ''',
            (user_id,)
        )
        teams = connection_manager.get_data(cursor, 'teams')

        cursor.execute(
            '''
            SELECT groups.group_id, groups.name
            FROM groups
            INNER JOIN usersgroups
            USING (group_id)
            WHERE user_id=%s;
            ''',
            (user_id,)
        )
        groups = connection_manager.get_data(cursor, 'groups')

        return_data = user_info
        return_data.update(phone_numbers)
        return_data.update(teams)
        return_data.update(groups)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved user', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
