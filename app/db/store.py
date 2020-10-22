from ..db.connection_manager import connection_manager


def create_store_item(team_id, name, price, active, modifiers, pictures):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO items (team_id, name, price, active)
            VALUES (%s, %s, %s, %s)
            RETURNING item_id;
            ''',
            (team_id, name, price, active)
        )
        return_data = connection_manager.get_data(cursor)

        for modifier in modifiers:
            cursor.execute(
                '''
                INSERT INTO itemmodifiers (item_id, modifier)
                VALUES (%s, %s);
                ''',
                (return_data['item_id'], modifier)
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
            DELETE FROM itemmodifiers
            WHERE item_id=%s;
            
            DELETE FROM items
            WHERE item_id=%s;
            ''',
            (item_id, item_id)
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


def edit_store_items_name(item_id, new_item_name):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE items
            SET name=%s
            WHERE item_id=%s;
            ''',
            (new_item_name, item_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited store items name', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_store_items_price(item_id, new_item_price):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE items
            SET price=%s
            WHERE item_id=%s;
            ''',
            (new_item_price, item_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited store items price', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_store_items_visibility(item_id, active):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE items
            SET active=%s
            WHERE item_id=%s;
            ''',
            (active, item_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited store items visibility', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_store_items_modifier(modifier_id, new_modifier):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE itemmodifiers
            SET modifier=%s
            WHERE modifier_id=%s;
            ''',
            (new_modifier, modifier_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully edited store items modifier', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def create_store_item_modifier(item_id, modifier):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO itemmodifiers (item_id, modifier)
            VALUES (%s, %s)
            RETURNING modifier_id;
            ''',
            (item_id, modifier)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created store item modifier', False, return_data)
        return res

    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_store_items_modifier(modifier_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            DELETE FROM itemmodifiers
            WHERE modifier_id=%s;
            ''',
            (modifier_id,)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed store items modifier', False, return_data)
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
            WHERE team_id=%s;
            ''',
            (team_id,)
        )

        store_items = []
        for row in connection_manager.get_data(cursor, 'store_items')['store_items']:
            cursor.execute(
                '''
                SELECT itemmodifiers.modifier_id, itemmodifiers.modifier
                FROM itemmodifiers
                INNER JOIN items
                USING (item_id)
                WHERE item_id=%s
                ''',
                (row['item_id'],)
            )
            modifiers = connection_manager.get_data(
                cursor, 'modifiers')

            cursor.execute(
                '''
                SELECT itempictures.picture_id, itempictures.image_url
                FROM itempictures
                INNER JOIN items
                USING (item_id)
                WHERE item_id=%s
                ''',
                (row['item_id'],)
            )
            pictures = connection_manager.get_data(
                cursor, 'pictures')

            row.update(modifiers)
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
