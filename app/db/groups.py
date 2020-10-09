def create_group(connection, name, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO groups (team_id, name)
            VALUES (%s, %s)
            RETURNING group_id;
            ''',
            (team_id, name)
        )

        result = ('successfully created group', 200, cursor.fetchone()[0])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def add_to_group(connection, user_id, group_id):
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

        result = ('successfully joined group', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def remove_from_group(connection, user_id, group_id):
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

        result = ('successfully left group', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


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
