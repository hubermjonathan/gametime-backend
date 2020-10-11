from ..db import runner


def create_team(connection, name, owner_user_id):
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

                INSERT INTO usersteams (user_id, team_id, permission_level, fund_goal, fund_current, fund_desc)
                VALUES (%s, new_team_id, 2, 0, 0, '');

                INSERT INTO groups (team_id, name)
                VALUES (new_team_id, 'All Members');
            END $$;

            SELECT team_id
            FROM teams
            WHERE name=%s AND owner=%s
            ORDER BY team_id DESC
            LIMIT 1;
            ''',
            (name, owner_user_id, owner_user_id, name, owner_user_id)
        )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully created team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def add_user_to_team(connection, user_id, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO usersteams (user_id, team_id, permission_level, fund_goal, fund_current, fund_desc)
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

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully added user to team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def remove_user_from_team(connection, user_id, team_id):
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

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully removed user from team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def change_users_permission_level_for_team(connection, user_id, team_id, permission_level):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE usersteams
            SET permission_level=%s
            WHERE user_id=%s AND team_id=%s;
            ''',
            (permission_level, user_id, team_id)
        )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully changed users permission level for team',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def edit_teams_name(connection, team_id, new_team_name):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET name=%s
            WHERE team_id=%s;
            ''',
            (new_team_name, team_id)
        )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully edited teams name', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def get_team(connection, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM teams
            WHERE team_id=%s;
            ''',
            (team_id,)
        )
        team_info = runner.get_data(cursor)

        cursor.execute(
            '''
            SELECT users.*, usersteams.permission_level
            FROM users
            INNER JOIN usersteams
            ON users.user_id=usersteams.user_id
            WHERE usersteams.team_id=%s;
            ''',
            (team_id,)
        )
        users = runner.get_data(cursor, 'users')

        return_data = team_info
        return_data.update(users)
        cursor.close()

        res = ('successfully retrieved team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def get_teams_phone_numbers(connection, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT users.phone_number
            FROM users
            INNER JOIN usersgroups
            USING (user_id)
            INNER JOIN groups
            USING (group_id)
            WHERE groups.team_id=%s AND groups.name='All Members';
            ''',
            (team_id,)
        )

        return_data = runner.get_data(cursor, 'phone_numbers')
        cursor.close()

        res = ('successfully retrieved teams phone numbers', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def get_teams_groups(connection, team_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM groups
            WHERE team_id=%s;
            ''',
            (team_id,)
        )

        groups = []
        for row in runner.get_data(cursor, 'groups')['groups']:
            cursor.execute(
                '''
                SELECT users.*
                FROM users
                INNER JOIN usersgroups
                ON users.user_id=usersgroups.user_id
                WHERE usersgroups.group_id=%s;
                ''',
                (row['group_id'],)
            )

            users = runner.get_data(cursor, 'users')
            users = {'users': []} if 'users' not in users else users
            row.update(users)
            groups.append(row)

        return_data = {
            'groups': groups
        }
        cursor.close()

        res = ('successfully retrieved teams groups', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res
