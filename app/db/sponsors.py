from ..db.connection_manager import connection_manager


def create_sponsor(team_id, name, active, picture):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO sponsors (team_id, name, picture, active)
            VALUES (%s, %s, %s, %s)
            RETURNING sponsor_id;
            ''',
            (team_id, name, picture, active)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created sponsor for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_sponsor(sponsor_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            REMOVE FROM sponsors
            WHERE sponsor_id=%s;
            ''',
            (sponsor_id,)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed sponsor for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_sponsors_for_team(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT sponsor_id, name, picture, active
            FROM sponsors
            WHERE team_id=%s;
            ''',
            (team_id,)
        )
        return_data = connection_manager.get_data(cursor, 'sponsors')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved sponsors for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
