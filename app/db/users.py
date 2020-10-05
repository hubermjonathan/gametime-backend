def create_user(connection, name, email, phone_number):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO users (name, email, phone_number)
            VALUES (%s, %s, %s)
            RETURNING user_id;
            ''',
            (name, email, phone_number)
        )

        result = ('successfully created user', 200, cursor.fetchone()[0])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def add_phone_number(connection, user_id, phone_number):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO phones (user_id, phone_number)
            VALUES (%s, %s);
            ''',
            (user_id, phone_number)
        )

        result = ('successfully added phone number', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def remove_phone_number(connection, user_id, phone_number):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            DELETE FROM phones
            WHERE user_id=%s AND phone_number=%s;
            ''',
            (user_id, phone_number)
        )

        result = ('successfully removed phone number', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_users_teams(connection, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT teams.team_id, teams.name
            FROM teams
            INNER JOIN usersteams
            ON teams.team_id=usersteams.team_id
            WHERE user_id=%s
            ''',
            (user_id,)
        )

        result = ('successfully retrieved teams', 200, cursor.fetchall())
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result
