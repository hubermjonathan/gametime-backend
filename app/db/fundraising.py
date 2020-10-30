from ..db.connection_manager import connection_manager


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
            SELECT fund_id, fund_goal, fund_current, fund_desc
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
            SELECT fund_id, fund_goal, fund_current, fund_desc
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
