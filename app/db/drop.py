def drop_test_tables(connection):
    try:
        cursor = connection.cursor()

        cursor.execute(open('app/db/schemas/test_schema.sql', 'r').read())

        result = ('successfully dropped and created tables', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def drop_prod_tables(connection):
    try:
        cursor = connection.cursor()

        cursor.execute(open('app/db/schemas/prod_schema.sql', 'r').read())

        result = ('successfully dropped and created tables', 200, [])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result
