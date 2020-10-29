from ..db.connection_manager import connection_manager


def create_store_item(team_id, name, price, active, types, pictures):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO items (team_id, name, price, active, archived)
            VALUES (%s, %s, %s, %s, false)
            RETURNING item_id;
            ''',
            (team_id, name, price, active)
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

        for picture in pictures:
            cursor.execute(
                '''
                INSERT INTO itempictures (item_id, image_url)
                VALUES (%s, %s);
                ''',
                (return_data['item_id'], picture)
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


def edit_store_item(item_id, name, price, active, types):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE items
            SET name=%s, price=%s, active=%s
            WHERE item_id=%s;
            ''',
            (name, price, active, item_id)
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


def create_store_item_picture(item_id, image_url):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO itempictures (item_id, image_url)
            VALUES (%s, %s)
            RETURNING picture_id;
            ''',
            (item_id, image_url)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created store item picture', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_store_items_picture(picture_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            DELETE FROM itempictures
            WHERE picture_id=%s;
            ''',
            (picture_id,)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed store items picture', False, return_data)
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

            cursor.execute(
                '''
                SELECT itempictures.picture_id, itempictures.image_url
                FROM itempictures
                INNER JOIN items
                USING (item_id)
                WHERE item_id=%s;
                ''',
                (row['item_id'],)
            )
            pictures = connection_manager.get_data(
                cursor, 'pictures')

            row.update(types)
            row.update(pictures)
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
