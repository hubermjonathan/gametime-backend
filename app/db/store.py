from ..db.connection_manager import connection_manager


def create_store_item(team_id, name, price, picture, active, types):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO items (team_id, name, price, picture, active, archived)
            VALUES (%s, %s, %s, %s, %s, false)
            RETURNING item_id;
            ''',
            (team_id, name, price, picture, active)
        )
        return_data = connection_manager.get_data(cursor)

        for t in types:
            cursor.execute(
                '''
                INSERT INTO itemtypes (item_id, label)
                VALUES (%s, %s);
                ''',
                (return_data['item_id'], t)
            )

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created store item', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_store_item(item_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE items
            SET archived=true
            WHERE item_id=%s;
            ''',
            (item_id,)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed store item', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_store_item(item_id, name, price, picture, active, types):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        if picture == '':
            cursor.execute(
                '''
                UPDATE items
                SET name=%s, price=%s, active=%s
                WHERE item_id=%s;
                ''',
                (name, price, active, item_id)
            )
        else:
            cursor.execute(
                '''
                UPDATE items
                SET name=%s, price=%s, picture=%s, active=%s
                WHERE item_id=%s;
                ''',
                (name, price, picture, active, item_id)
            )

        cursor.execute(
            '''
            DELETE FROM itemtypes
            WHERE item_id=%s;
            ''',
            (item_id,)
        )

        for t in types:
            cursor.execute(
                '''
                INSERT INTO itemtypes (item_id, label)
                VALUES (%s, %s);
                ''',
                (item_id, t)
            )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited store item', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_teams_store_items(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM items
            WHERE team_id=%s AND archived=false;
            ''',
            (team_id,)
        )

        store_items = []
        for row in connection_manager.get_data(cursor, 'store_items')['store_items']:
            cursor.execute(
                '''
                SELECT itemtypes.type_id, itemtypes.label
                FROM itemtypes
                INNER JOIN items
                USING (item_id)
                WHERE item_id=%s;
                ''',
                (row['item_id'],)
            )
            types = connection_manager.get_data(
                cursor, 'types')

            row.update(types)
            store_items.append(row)

        return_data = {
            'store_items': store_items
        }
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved store items', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
