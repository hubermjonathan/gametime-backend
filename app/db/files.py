from ..db.connection_manager import connection_manager
import boto3
from os import environ
import base64


AWS = boto3.resource(
    's3',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY')
)


def upload_file(file, name, is_photo):
    file_base64 = file[23:] if is_photo else file[28:]
    file_name = f'{name}.jpeg' if is_photo else f'{name}.pdf'
    obj = AWS.Object('gametime-file-storage', file_name)
    obj.put(Body=base64.b64decode(file_base64), ACL='public-read')
    url = f'https://gametime-file-storage.s3-us-east-2.amazonaws.com/{file_name}'
    return url


def create_file(team_id, user_id, file):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO files (team_id, user_id)
            VALUES (%s, %s)
            RETURNING file_id;
            ''',
            (team_id, user_id)
        )
        file_id = connection_manager.get_data(cursor)

        url = upload_file(file, file_id['file_id'], False)

        cursor.execute(
            '''
            UPDATE files
            SET url=%s
            WHERE file_id=%s
            RETURNING file_id, url;
            ''',
            (url, file_id['file_id'])
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


def create_photo(team_id, user_id, picture, active):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO files (team_id, user_id, active)
            VALUES (%s, %s, %s)
            RETURNING file_id;
            ''',
            (team_id, user_id, active)
        )
        file_id = connection_manager.get_data(cursor)

        url = upload_file(picture, file_id['file_id'], True)

        cursor.execute(
            '''
            UPDATE files
            SET url=%s
            WHERE file_id=%s
            RETURNING file_id, url;
            ''',
            (url, file_id['file_id'])
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
            DELETE FROM files
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
            WHERE team_id=%s AND active IS NOT NULL;
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
