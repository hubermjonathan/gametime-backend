from ..db.connection_manager import connection_manager


def create_file(team_id, user_id, url):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO files (team_id, user_id, url)
            VALUES (%s, %s, %s)
            RETURNING file_id;
            ''',
            (team_id, user_id, url)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created file', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def create_photo(team_id, user_id, url, active):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO files (team_id, user_id, url, active)
            VALUES (%s, %s, %s, %s)
            RETURNING file_id;
            ''',
            (team_id, user_id, url, active)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created photo', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_file(file_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            REMOVE FROM files
            WHERE file_id=%s;
            ''',
            (file_id,)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed file', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_photo(file_id, active):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE files
            SET active=%s
            WHERE file_id=%s;
            ''',
            (active, file_id)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully updated photo', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_files_for_team(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT file_id, url
            FROM files
            WHERE team_id=%s AND active IS NULL;
            ''',
            (team_id,)
        )
        return_data = connection_manager.get_data(cursor, 'files')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved files for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_files_for_user(team_id, user_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT file_id, url
            FROM files
            WHERE team_id=%s AND user_id=%s AND active IS NULL;
            ''',
            (team_id, user_id)
        )
        return_data = connection_manager.get_data(cursor, 'files')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved files for user', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_photos_for_team(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT file_id, url, active
            FROM files
            WHERE team_id=%s AND active IS NULL;
            ''',
            (team_id,)
        )
        return_data = connection_manager.get_data(cursor, 'photos')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved photos for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_photos_for_user(team_id, user_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT file_id, url, active
            FROM files
            WHERE team_id=%s AND user_id=%s;
            ''',
            (team_id, user_id)
        )
        return_data = connection_manager.get_data(cursor, 'photos')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved photos for user', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
