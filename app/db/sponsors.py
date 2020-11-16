from ..db.connection_manager import connection_manager
import boto3
from os import environ
import base64


AWS = boto3.resource(
    's3',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY')
)


def upload_picture(picture, id):
    picture_base64 = picture[23:]
    obj = AWS.Object('gametime-file-storage', f'{id}.jpeg')
    obj.put(Body=base64.b64decode(picture_base64), ACL='public-read')
    url = f'https://gametime-file-storage.s3-us-east-2.amazonaws.com/{id}.jpeg'
    return url


def create_sponsor(team_id, name, picture):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO sponsors (team_id, name)
            VALUES (%s, %s)
            RETURNING sponsor_id;
            ''',
            (team_id, name)
        )
        return_data = connection_manager.get_data(cursor)

        url = upload_picture(picture, return_data['sponsor_id'])

        cursor.execute(
            '''
            UPDATE sponsors
            SET picture=%s
            WHERE sponsor_id=%s;
            ''',
            (url, return_data['sponsor_id'])
        )

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created sponsor for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_sponsor(sponsor_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            DELETE FROM sponsors
            WHERE sponsor_id=%s;
            ''',
            (sponsor_id,)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed sponsor for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_sponsors_for_team(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT sponsor_id, name, picture
            FROM sponsors
            WHERE team_id=%s;
            ''',
            (team_id,)
        )
        return_data = connection_manager.get_data(cursor, 'sponsors')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved sponsors for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
