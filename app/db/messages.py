from ..db import runner
from datetime import datetime


def create_direct_message(connection, recipient_user_id, sender_user_id, message_content):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
                INSERT INTO messages (user_id, sender_id, content, time_sent)
                VALUES (%s, %s, %s, %s)
                RETURNING message_id;
            ''',
            (recipient_user_id, sender_user_id, message_content, datetime.now())
        )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully created direct message', 200, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def create_group_message(connection, recipient_group_id, sender_user_id, message_content):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
                INSERT INTO groupmessages (group_id, sender_id, content, time_sent)
                VALUES (%s, %s, %s, %s)
                RETURNING gmessage_id;
            ''',
            (recipient_group_id, sender_user_id, message_content, datetime.now())
        )

        return_data = runner.get_data(cursor)
        cursor.close()

        res = ('successfully created group message', 200, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def get_users_direct_messages(connection, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM messages
            WHERE user_id=%s
            ORDER BY time_sent
            ASC;
            ''',
            (user_id,)
        )

        return_data = runner.get_data(cursor, 'messages')
        cursor.close()

        res = ('successfully retrieved direct messages', 200, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res


def get_groups_messages(connection, group_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM groupmessages
            WHERE group_id=%s
            ORDER BY time_sent
            ASC;
            ''',
            (group_id,)
        )

        return_data = runner.get_data(cursor, 'messages')
        cursor.close()

        res = ('successfully retrieved group messages', 200, return_data)
        return res
    except Exception as e:
        cursor.close()
        res = (str(e), True, {})
        return res
