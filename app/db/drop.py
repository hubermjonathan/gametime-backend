def drop_test_tables(connection):
    try:
        cursor = connection.cursor()

        cursor.execute(open('app/db/schemas/test_schema.sql', 'r').read())

        data = {
            'data': None
        }

        result = ('successfully dropped and created test tables', 200, data)
        cursor.close()
        return result
    except Exception as e:
        data = {
            'data': None
        }

        result = (str(e), 500, data)
        cursor.close()
        return result


def drop_prod_tables(connection):
    try:
        cursor = connection.cursor()

        cursor.execute(open('app/db/schemas/prod_schema.sql', 'r').read())

        data = {
            'data': None
        }

        result = ('successfully dropped and created prod tables', 200, data)
        cursor.close()
        return result
    except Exception as e:
        data = {
            'data': None
        }

        result = (str(e), 500, data)
        cursor.close()
        return result
