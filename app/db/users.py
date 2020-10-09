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


def get_user_id(connection, email):
    try:
        cursor = connection.cursor()

        print(email)

        cursor.execute( 
            '''
            SELECT email
            FROM users;
            '''
        )

        print(cursor.fetchall())


        cursor.execute(
            '''
            SELECT user_id
            FROM users
            WHERE email=%s;
            ''',
            (email,)
        )

        #print('CURSOR VAL\n\n:' ,cursor.fetchall())

        result = ('successfully retrieved user id', 200, cursor.fetchone()[0])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result

def check_phone_number_exists(connection, user_id, phone_number):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT * FROM phones
            WHERE user_id = %s
            AND phone_number = %s
            ''',
            (user_id, phone_number)
        )

        result = ('checked for duplicates', 200, cursor.fetchall())
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


def get_user(connection, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM users
            WHERE user_id=%s
            ''',
            (user_id,)
        )
        user_info = cursor.fetchone()

        cursor.execute(
            '''
            SELECT phone_number
            FROM phones
            WHERE user_id=%s
            ''',
            (user_id,)
        )
        phone_numbers = cursor.fetchall()
        phone_numbers = [phone[0] for phone in phone_numbers]
        data = user_info + (phone_numbers,)

        result = ('successfully retrieved user', 200, data)
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
            SELECT teams.team_id, teams.name, usersteams.privilege_level
            FROM teams
            INNER JOIN usersteams
            ON teams.team_id=usersteams.team_id
            WHERE user_id=%s
            ''',
            (user_id,)
        )

        data = []
        columns = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            formatted_row = {}
            for i, col in enumerate(columns):
                formatted_row[col] = row[i]
            data.append(formatted_row)

        result = ('successfully retrieved teams', 200, data)
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_users_groups(connection, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT groups.group_id, groups.name
            FROM groups
            INNER JOIN usersgroups
            ON groups.group_id=usersgroups.group_id
            WHERE user_id=%s
            ''',
            (user_id,)
        )

        result = ('successfully retrieved groups', 200, cursor.fetchall())
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result

def get_users_phone_number(connection, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT phone_number
            FROM users
            WHERE user_id=%s
            ''',
            (user_id,)
        )

        result = ('successfully retrieved phone number', 200, cursor.fetchone()[0])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result
