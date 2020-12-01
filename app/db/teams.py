from ..db.connection_manager import connection_manager


def create_team(name, owner_user_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO teams (name, owner, account_id)
            VALUES (%s, %s, %s)
            RETURNING team_id;
            ''',
            (name, owner_user_id, account_id)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.execute(
            '''
            INSERT INTO usersteams (user_id, team_id, permission_level)
            VALUES (%s, %s, 2);
            ''',
            (owner_user_id, return_data['team_id'])
        )

        cursor.execute(
            '''
            INSERT INTO groups (team_id, name)
            VALUES (%s, 'All Members');
            ''',
            (return_data['team_id'],)
        )

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def add_user_to_team(user_id, team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO usersteams (user_id, team_id, permission_level)
            VALUES (%s, %s, 0);

            INSERT INTO usersgroups (user_id, group_id)
            VALUES (%s, (
                SELECT group_id
                FROM groups
                WHERE team_id=%s AND name='All Members'
            ));
            ''',
            (user_id, team_id, user_id, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully added user to team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_user_from_team(user_id, team_id):
    try:
        connection = connection_manager.connect()
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

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed user from team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_users_permission_level_for_team(user_id, team_id, permission_level):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE usersteams
            SET permission_level=%s
            WHERE user_id=%s AND team_id=%s;
            ''',
            (permission_level, user_id, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully changed users permission level for team',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_users_permission_level_for_team(user_id, team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT permission_level
            FROM usersteams
            WHERE user_id=%s AND team_id=%s;
            ''',
            (user_id, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved users permission level for team',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_teams_name(team_id, new_team_name):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET name=%s
            WHERE team_id=%s;
            ''',
            (new_team_name, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited teams name', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_team(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM teams
            WHERE team_id=%s;
            ''',
            (team_id,)
        )
        team_info = connection_manager.get_data(cursor)

        cursor.execute(
            '''
            SELECT users.*, usersteams.permission_level
            FROM users
            INNER JOIN usersteams
            USING (user_id)
            WHERE usersteams.team_id=%s;
            ''',
            (team_id,)
        )
        users = connection_manager.get_data(cursor, 'users')

        return_data = team_info
        return_data.update(users)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res

def get_team_account(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT account_id
            FROM teams
            WHERE team_id=%s;
            ''',
            (team_id,)
        )
        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res

def update_bank_account(team_id, bank_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET bank_id=%s
            WHERE team_id=%s;
            ''',
            (bank_id, team_id,)
        )
        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully updated bank account', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res

def get_all_teams():
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT name, team_id
            FROM teams;
            '''
        )

        return_data = connection_manager.get_data(cursor, 'teams')
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved all teams', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res

def get_teams_phone_numbers(team_id):
    try:
        connection = connection_manager.connect()
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

        return_data = connection_manager.get_data(cursor, 'phone_numbers')
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved teams phone numbers', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_teams_groups(team_id):
    try:
        connection = connection_manager.connect()
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
        for row in connection_manager.get_data(cursor, 'groups')['groups']:
            cursor.execute(
                '''
                SELECT users.*
                FROM users
                INNER JOIN usersgroups
                USING (user_id)
                WHERE usersgroups.group_id=%s;
                ''',
                (row['group_id'],)
            )
            users = connection_manager.get_data(cursor, 'users')

            row.update(users)
            groups.append(row)

        return_data = {
            'groups': groups
        }
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved teams groups', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_teams_coach(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT users.email
            FROM teams
            INNER JOIN users
            ON users.user_id=teams.owner
            WHERE team_id=%s;
            ''',
            (team_id,)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved teams coach', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
