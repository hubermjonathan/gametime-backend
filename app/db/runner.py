def get_data(cursor, key_name='results'):
    if (cursor.description is None):
        cursor.close()
        return {}

    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()

    if (len(results) == 0):
        pass
    elif (len(results) == 1):
        data = {}
        for i, col in enumerate(columns):
            data[col] = results[0][i]
    else:
        data = {
            key_name: []
        }
        for row in results:
            formatted_row = {}
            for i, col in enumerate(columns):
                formatted_row[col] = row[i]
            data[key_name].append(formatted_row)

    cursor.close()
    return data
