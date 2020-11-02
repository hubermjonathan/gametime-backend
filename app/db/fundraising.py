from ..db.connection_manager import connection_manager
from datetime import datetime

def print_all_team_fundraisers():
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM teams
            ''',
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        print(return_data)

        res = ('successfully got user fund id', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res

def print_all_user_fundraisers():
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM usersteams
            ''',
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        print(return_data)

        res = ('successfully got user fund id', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res

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
            (team_id)
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

def edit_teams_fundraiser(fund_id, goal, current, description):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET fund_goal=%s, fund_current=%s, fund_desc=%s
            WHERE fund_id=%s;
            ''',
            (goal, current, description, fund_id)
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


def edit_users_fundraiser(fund_id, goal, current, description):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE usersteams
            SET fund_goal=%s, fund_current=%s, fund_desc=%s
            WHERE fund_id=%s;
            ''',
            (goal, current, description, fund_id)
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


def get_teams_fundraiser(fund_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT fund_id, fund_goal, fund_current, fund_desc, fund_start, fund_end
            FROM teams
            WHERE fund_id=%s;
            ''',
            (fund_id,)
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


def get_users_fundraiser(fund_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT fund_id, fund_goal, fund_current, fund_desc, fund_start, fund_end
            FROM usersteams
            WHERE fund_id=%s;
            ''',
            (fund_id,)
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


def start_teams_fundraiser(fund_id, end_date):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE teams
            SET fund_start=%s, fund_end=%s
            WHERE fund_id=%s;
            ''',
            (datetime.now(), datetime.fromtimestamp(end_date / 1000), fund_id)
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


def start_users_fundraiser(fund_id, end_date):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE usersteams
            SET fund_start=%s, fund_end=%s
            WHERE fund_id=%s;
            ''',
            (datetime.now(), datetime.fromtimestamp(end_date / 1000), fund_id)
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
