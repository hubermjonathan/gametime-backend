from ..db.connection_manager import connection_manager


def create_promotion(team_id, name, description, picture, start_time, end_time):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO promotions (team_id, name, description, picture, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING promotion_id;
            ''',
            (team_id, name, description, picture, start_time, end_time)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created promotion for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_promotion(promotion_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            REMOVE FROM promotions
            WHERE promotion_id=%s;
            ''',
            (promotion_id,)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed promotion for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_promotions_for_team(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT promotion_id, name, description, picture, start_time, end_time
            FROM promotions
            WHERE team_id=%s AND CURRENT_TIMESTAMP BETWEEN start_time AND end_time;
            ''',
            (team_id,)
        )
        return_data = connection_manager.get_data(cursor, 'promotions')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved promotions for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
