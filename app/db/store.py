from ..db.connection_manager import connection_manager


def create_store_item(team_id, name, price, modifiers):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO items (team_id, name, price)
            VALUES (%s, %s, %s)
            RETURNING item_id;
            ''',
            (team_id, name, price)
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
            item_modifiers = connection_manager.get_data(
                cursor, 'item_modifiers')

            row.update(item_modifiers)
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
