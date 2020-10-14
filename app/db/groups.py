from ..db.connection_manager import connection_manager


def create_group(name, parent_team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO groups (team_id, name)
            VALUES (%s, %s)
            RETURNING group_id;
            ''',
            (parent_team_id, name)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def add_user_to_group(user_id, group_id):
    try:
        connection = connection_manager.connect()
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

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully added user(s) to group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_user_from_group(user_id, group_id):
    try:
        connection = connection_manager.connect()
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

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed user(s) from group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_group(group_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM groups
            WHERE group_id=%s;
            ''',
            (group_id,)
        )
        group_info = connection_manager.get_data(cursor)

        cursor.execute(
            '''
            SELECT users.*
            FROM users
            INNER JOIN usersgroups
           	USING (user_id)
            WHERE usersgroups.group_id=%s;
            ''',
            (group_id,)
        )
        users = connection_manager.get_data(cursor, 'users')

        return_data = group_info
        return_data.update(users)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved group', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_groups_phone_numbers(group_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT users.phone_number
            FROM users
            INNER JOIN usersgroups
            USING (user_id)
            WHERE usersgroups.group_id=%s;
            ''',
            (group_id,)
        )

        return_data = connection_manager.get_data(cursor, 'phone_numbers')
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved groups phone numbers', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
