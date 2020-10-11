def get_data(cursor, key_name='results'):
    if (cursor.description is None):
        return {}

    columns = [desc[0] for desc in cursor.description]
    results = cursor.fetchall()

    if (len(results) == 0):
        return {}
    elif (len(results) == 1 and key_name == 'results'):
        data = {}
        for i, col in enumerate(columns):
            data[col] = results[0][i]
    else:
        data = {
            key_name: []
        }
        for row in results:
            if (len(row) == 1):
                data[key_name].append(row[0])
            else:
                formatted_row = {}
                for i, col in enumerate(columns):
                    formatted_row[col] = row[i]
                data[key_name].append(formatted_row)

    return data
