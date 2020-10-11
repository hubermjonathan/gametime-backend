from ..db import runner


def reset_tables(connection, database):
    try:
        cursor = connection.cursor()

        schema = 'app/db/schemas/prod_schema.sql' if database == 'prod' else 'app/db/schemas/test_schema.sql'
        cursor.execute(open(schema, 'r').read())

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully dropped and created tables', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res
