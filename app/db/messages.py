from datetime import datetime


def create_message(connection, recipient_id, sender_id, content):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
                INSERT INTO messages (user_id, sender_id, content, time_sent)
                VALUES (%s, %s, %s, %s)
                RETURNING message_id;
            ''',
            (recipient_id, sender_id, content, datetime.now())
        )

        result = ('successfully created message', 200, cursor.fetchone()[0])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def create_group_message(connection, recipient_id, sender_id, content):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
                INSERT INTO groupmessages (group_id, sender_id, content, time_sent)
                VALUES (%s, %s, %s, %s)
                RETURNING gmessage_id;
            ''',
            (recipient_id, sender_id, content, datetime.now())
        )

        result = ('successfully created group message',
                  200, cursor.fetchone()[0])
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_messages(connection, user_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM messages
            WHERE user_id=%s
            ORDER BY time_sent
            ASC
            ''',
            (user_id,)
        )

        result = ('successfully retrieved messages', 200, cursor.fetchall())
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result


def get_group_messages(connection, group_id):
    try:
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM groupmessages
            WHERE group_id=%s
            ORDER BY time_sent
            ASC
            ''',
            (group_id,)
        )

        result = ('successfully retrieved messages', 200, cursor.fetchall())
        cursor.close()
        return result
    except Exception as e:
        result = (str(e), 500, [])
        cursor.close()
        return result
