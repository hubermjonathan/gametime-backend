def create_team(connection, name, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            DO $$
            DECLARE new_team_id integer;
            BEGIN
                INSERT INTO teams (name, fund_goal, fund_current, fund_desc, account_number, routing_number, owner)
                VALUES (%s, 0, 0, '', 0, 0, %s)
                RETURNING team_id INTO new_team_id;

                INSERT INTO usersteams (user_id, team_id, privelege_level, fund_goal, fund_current, fund_desc)
                VALUES (%s, new_team_id, 2, 0, 0, '');

                INSERT INTO groups (team_id, name)
                VALUES (new_team_id, 'All Members');
            END $$;

            SELECT team_id
            FROM teams
            WHERE name=%s AND owner=%s
            ORDER BY team_id DESC;
            ''',
            (name, user_id, user_id, name, user_id)
        )

        result = ('successfully created team', 200, cursor.fetchone()[0])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def add_to_team(connection, user_id, team_id):
    try:
        cursor = connection.cursor()

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

        result = ('successfully joined team', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def remove_from_team(connection, user_id, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            DELETE FROM usersteams
            WHERE user_id=%s AND team_id=%s;

            DELETE FROM usersgroups
            USING (
                SELECT group_id
                FROM groups
                WHERE team_id=%s
            ) AS joinedgroups
            WHERE usersgroups.user_id=%s AND usersgroups.group_id=joinedgroups.group_id;
            ''',
            (user_id, team_id, team_id, user_id)
        )

        result = ('successfully left team', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def change_permission_level(connection, user_id, team_id, privelege_level):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE usersteams
            SET privelege_level=%s
            WHERE user_id=%s AND team_id=%s;
            ''',
            (privelege_level, user_id, team_id)
        )

        result = ('successfully changed permission level', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def edit_team_name(connection, team_id, name):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET name=%s
            WHERE team_id=%s;
            ''',
            (name, team_id)
        )

        result = ('successfully edited team name', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_team(connection, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM teams
            WHERE team_id=%s
            ''',
            (team_id,)
        )

        result = ('successfully retrieved team', 200, cursor.fetchall())
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_teams_members(connection, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT users.*, usersteams.privelege_level
            FROM users
            INNER JOIN usersteams
            ON users.user_id=usersteams.user_id
            WHERE usersteams.team_id=%s
            ''',
            (team_id,)
        )

        result = ('successfully retrieved members', 200, cursor.fetchall())
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_teams_phone_numbers(connection, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT owner
            FROM teams
            WHERE team_id=%s;
            ''',
            (team_id,)
        )

        owner_id = cursor.fetchone()[0]
        cursor.execute(
            '''
            SELECT users.phone_number
            FROM users
            INNER JOIN usersteams
            ON users.user_id=usersteams.user_id
            WHERE usersteams.team_id=%s AND NOT users.user_id=%s;
            ''',
            (team_id, owner_id)
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


def get_teams_groups(connection, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM groups
            WHERE team_id=%s
            ''',
            (team_id,)
        )

        data = []
        columns = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            formatted_row = {}
            for i, col in enumerate(columns):
                formatted_row[col] = row[i]

            cursor2 = connection.cursor()
            cursor2.execute(
                '''
                SELECT users.*
                FROM users
                INNER JOIN usersgroups
                ON users.user_id=usersgroups.user_id
                WHERE usersgroups.group_id=%s
                ''',
                (row[0],)
            )

            group_members = cursor2.fetchall()
            formatted_row['members'] = group_members
            data.append(formatted_row)
            cursor2.close()

        result = ('successfully retrieved groups', 200, data)
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result
