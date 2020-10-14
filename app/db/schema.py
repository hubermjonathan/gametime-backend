from ..db.connection_manager import connection_manager


def reset_tables(database):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        schema = 'app/db/schemas/prod_schema.sql' if database == 'prod' else 'app/db/schemas/test_schema.sql'
        cursor.execute(open(schema, 'r').read())

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully dropped and created tables', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
