from ..db import runner


def create_group(connection, new_group_name, parent_team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO groups (team_id, name)
            VALUES (%s, %s)
            RETURNING group_id;
            ''',
            (parent_team_id, new_group_name)
        )

        return_data = runner.get_data(cursor)

        res = ('successfully created group', False, return_data)
        return res
    except Exception as e:
        return_data = runner.get_data(cursor)
        res = (str(e), True, return_data)
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

        res = ('successfully added user(s) to group', False, return_data)
        return res
    except Exception as e:
        return_data = runner.get_data(cursor)
        res = (str(e), True, return_data)
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

        res = ('successfully removed user(s) from group', False, return_data)
        return res
    except Exception as e:
        return_data = runner.get_data(cursor)
        res = (str(e), True, return_data)
        return res


def get_groups_members(connection, group_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT users.*
            FROM users
            INNER JOIN usersgroups
            ON users.user_id=usersgroups.user_id
            WHERE usersgroups.group_id=%s
            ''',
            (group_id,)
        )

        result = ('successfully retrieved members', 200, cursor.fetchall())
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_groups_phone_numbers(connection, group_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT users.phone_number
            FROM users
            INNER JOIN usersgroups
            ON users.user_id=usersgroups.user_id
            WHERE usersgroups.group_id=%s
            ''',
            (group_id,)
        )

        data = cursor.fetchall()
        data = [phone_number[0] for phone_number in data]

        result = ('successfully retrieved phone numbers', 200, data)
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_group(connection, group_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM groups
            WHERE group_id=%s
            ''',
            (group_id,)
        )
        group_info = cursor.fetchone()

        cursor.execute(
            '''
            SELECT users.*
            FROM users
            INNER JOIN usersgroups
            ON users.user_id=usersgroups.user_id
            WHERE usersgroups.group_id=%s
            ''',
            (group_id,)
        )
        group_members = cursor.fetchall()
        group_members_ids = [user[0] for user in group_members]
        data = group_info + (group_members_ids,)

        result = ('successfully retrieved group', 200, data)
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result
