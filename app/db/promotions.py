from ..db.connection_manager import connection_manager
import boto3
from os import environ
import base64
from datetime import datetime


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


def create_promotion(team_id, name, description, picture, start_time, end_time):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO promotions (team_id, name, description, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING promotion_id;
            ''',
            (team_id, name, description, datetime.fromtimestamp(start_time), datetime.fromtimestamp(end_time))
        )
        return_data = connection_manager.get_data(cursor)

        url = upload_picture(picture, return_data['promotion_id'])

        cursor.execute(
            '''
            UPDATE promotions
            SET picture=%s
            WHERE promotion_id=%s;
            ''',
            (url, return_data['promotion_id'])
        )

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created promotion for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def remove_promotion(promotion_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            DELETE FROM promotions
            WHERE promotion_id=%s;
            ''',
            (promotion_id,)
        )
        return_data = connection_manager.get_data(cursor)

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully removed promotion for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_promotions_for_team(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT promotion_id, name, description, picture, start_time, end_time
            FROM promotions
            WHERE team_id=%s AND %s BETWEEN start_time AND end_time;
            ''',
            (team_id, datetime.now())
        )
        return_data = connection_manager.get_data(cursor, 'promotions')

        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved promotions for team', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
