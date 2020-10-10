def drop_test_tables(connection):
    try:
        cursor = connection.cursor()

        cursor.execute(open('app/db/schemas/test_schema.sql', 'r').read())

        return_data = {
            'data': None
        }

        res = ('successfully dropped and created test tables', 200, return_data)
        cursor.close()
        return res
    except Exception as e:
        return_data = {
            'data': None
        }

        res = (str(e), 500, return_data)
        cursor.close()
        return res


def drop_prod_tables(connection):
    try:
        cursor = connection.cursor()

        cursor.execute(open('app/db/schemas/prod_schema.sql', 'r').read())

        return_data = {
            'data': None
        }

        res = ('successfully dropped and created prod tables', 200, return_data)
        cursor.close()
        return res
    except Exception as e:
        return_data = {
            'data': None
        }

        res = (str(e), 500, return_data)
        cursor.close()
        return res
