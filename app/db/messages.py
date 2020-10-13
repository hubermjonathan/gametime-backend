from ..db.connection_manager import connection_manager
from datetime import datetime


def create_direct_message(recipient_user_id, sender_user_id, message_content):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
                INSERT INTO messages (user_id, sender_id, content, time_sent)
                VALUES (%s, %s, %s, %s)
                RETURNING message_id;
            ''',
            (recipient_user_id, sender_user_id, message_content, datetime.now())
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created direct message', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def create_group_message(recipient_group_id, sender_user_id, message_content):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
                INSERT INTO groupmessages (group_id, sender_id, content, time_sent)
                VALUES (%s, %s, %s, %s)
                RETURNING gmessage_id;
            ''',
            (recipient_group_id, sender_user_id, message_content, datetime.now())
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created group message', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_users_direct_messages(user_id):
    try:
        connection = connection_manager.connect()
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

        return_data = connection_manager.get_data(cursor, 'messages')
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved direct messages', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_groups_messages(group_id):
    try:
        connection = connection_manager.connect()
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

        return_data = connection_manager.get_data(cursor, 'messages')
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved group messages', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
