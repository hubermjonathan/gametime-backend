from ..db.connection_manager import connection_manager
from datetime import datetime


def get_user_fund_id(user_id, team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT fund_id
            FROM usersteams
            WHERE user_id=%s
            AND team_id=%s;
            ''',
            (user_id, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully got user fund id', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_team_fund_id(user_id, team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT fund_id
            FROM teams
            WHERE team_id=%s;
            ''',
            (team_id,)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully got team fund id', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_teams_fundraiser(team_id, goal, current, description, end_time):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET fund_goal=%s, fund_current=%s, fund_desc=%s, fund_end=%s
            WHERE team_id=%s;
            ''',
            (goal, current, description, datetime.fromtimestamp(end_time), team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited teams fundraiser', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_users_fundraiser(user_id, team_id, goal, current, description, end_time):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE usersteams
            SET fund_goal=%s, fund_current=%s, fund_desc=%s, fund_end=%s
            WHERE user_id=%s AND team_id=%s;
            ''',
            (goal, current, description, datetime.fromtimestamp(end_time), user_id, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited users fundraiser for team',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_teams_fundraiser(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT name, fund_id, fund_goal, fund_current, fund_desc, fund_start, fund_end
            FROM teams
            WHERE team_id=%s;
            ''',
            (team_id,)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved teams fundraiser information',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_users_fundraiser(user_id, team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT fund_id, fund_goal, fund_current, fund_desc, fund_start, fund_end
            FROM usersteams
            WHERE user_id=%s AND team_id=%s;
            ''',
            (user_id, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved users fundraiser information for a team',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def start_teams_fundraiser(team_id, start_date, end_date, goal, description):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET fund_start=%s, fund_end=%s, fund_goal=%s, fund_current=%s, fund_desc=%s
            WHERE team_id=%s;
            ''',
            (datetime.fromtimestamp(start_date), datetime.fromtimestamp(end_date), goal, 0, description, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully started teams fundraiser',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def start_users_fundraiser(user_id, team_id, start_date, end_date, goal, description):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE usersteams
            SET fund_start=%s, fund_end=%s, fund_goal=%s, fund_current=%s, fund_desc=%s
            WHERE user_id=%s AND team_id=%s;
            ''',
            (datetime.fromtimestamp(start_date), datetime.fromtimestamp(end_date), goal, 0, description, user_id, team_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully started users fundraiser for team',
               False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_teams_fundraiser_report(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT name, fund_id, fund_goal, fund_current, fund_desc, fund_start, fund_end
            FROM teams
            WHERE team_id=%s;
            ''',
            (team_id,)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.execute(
            '''
            SELECT users.first_name, users.last_name, usersteams.fund_id, usersteams.fund_goal, usersteams.fund_current, usersteams.fund_desc, usersteams.fund_start, usersteams.fund_end
            FROM usersteams
            INNER JOIN users
            USING (user_id)
            WHERE usersteams.team_id=%s;
            ''',
            (team_id,)
        )
        player_data = connection_manager.get_data(cursor, 'player_data')
        return_data.update(player_data)

        cursor.execute(
            '''
            SELECT transaction_id, amount, buyer_email, time_purchased
            FROM transactions
            WHERE team_id=%s AND buyer_address IS NULL;
            ''',
            (team_id,)
        )
        transactions = connection_manager.get_data(cursor, 'transactions')
        return_data.update(transactions)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved teams fundraiser report', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
