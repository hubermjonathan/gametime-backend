from ..db import runner


def reset_tables(connection, database):
    try:
        cursor = connection.cursor()

        schema = 'app/db/schemas/prod_schema.sql' if database == 'prod' else 'app/db/schemas/test_schema.sql'
        cursor.execute(open(schema, 'r').read())

        return_data = runner.get_data(cursor)

        res = ('successfully dropped and created tables', 200, return_data)
        return res
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result
