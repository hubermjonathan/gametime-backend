from ..db import runner


def reset_tables(connection, database):
    try:
        cursor = connection.cursor()

        schema = 'app/db/schemas/prod_schema.sql' if database == 'prod' else 'app/db/schemas/test_schema.sql'
        cursor.execute(open(schema, 'r').read())

        return_data = runner.get_data(cursor)

        res = ('successfully dropped and created tables', False, return_data)
        return res
    except Exception as e:
        return_data = runner.get_data(cursor)
        res = (str(e), True, return_data)
        return res
