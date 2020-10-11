from ..db import runner


def create_group(connection, name, parent_team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO groups (team_id, name)
            VALUES (%s, %s)
            RETURNING group_id;
            ''',
            (parent_team_id, name)
        )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully created group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def add_user_to_group(connection, user_id, group_id):
    try:
        cursor = connection.cursor()

        if isinstance(user_id, list):
            for user in user_id:
                cursor.execute(
                    '''
                    INSERT INTO usersgroups (user_id, group_id)
                    VALUES (%s, %s);
                    ''',
                    (user, group_id)
                )
        else:
            cursor.execute(
                '''
                INSERT INTO usersgroups (user_id, group_id)
                VALUES (%s, %s);
                ''',
                (user_id, group_id)
            )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully added user(s) to group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def remove_user_from_group(connection, user_id, group_id):
    try:
        cursor = connection.cursor()

        if isinstance(user_id, list):
            for user in user_id:
                cursor.execute(
                    '''
                    DELETE FROM usersgroups
                    WHERE user_id=%s AND group_id=%s;
                    ''',
                    (user, group_id)
                )
        else:
            cursor.execute(
                '''
                DELETE FROM usersgroups
                WHERE user_id=%s AND group_id=%s;
                ''',
                (user_id, group_id)
            )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully removed user(s) from group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def get_group(connection, group_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM groups
            WHERE group_id=%s;
            ''',
            (group_id,)
        )
        group_info = runner.get_data(cursor)

        cursor.execute(
            '''
            SELECT users.*
            FROM users
            INNER JOIN usersgroups
            ON users.user_id=usersgroups.user_id
            WHERE usersgroups.group_id=%s;
            ''',
            (group_id,)
        )
        users = runner.get_data(cursor, 'users')

        return_data = group_info
        return_data.update(users)
        cursor.close()

        res = ('successfully retrieved group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def get_groups_phone_numbers(connection, group_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT users.phone_number
            FROM users
            INNER JOIN usersgroups
            ON users.user_id=usersgroups.user_id
            WHERE usersgroups.group_id=%s;
            ''',
            (group_id,)
        )

        return_data = runner.get_data(cursor, 'phone_numbers')

        res = ('successfully retrieved groups phone numbers', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res
