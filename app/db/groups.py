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
