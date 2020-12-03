from ..db.connection_manager import connection_manager
from datetime import datetime


def create_transaction(team_id, buyer_email, buyer_address, items, amount):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            INSERT INTO transactions (team_id, status, amount, buyer_email, buyer_address, time_purchased)
            VALUES (%s, 0, %s, %s, %s, %s)
            RETURNING transaction_id;
            ''',
            (team_id, amount, buyer_email, buyer_address, datetime.now())
        )
        transaction_info = connection_manager.get_data(cursor)

        for item in items:
            cursor.execute(
                '''
                INSERT INTO transactionsitems (transaction_id, item_id, label, quantity)
                VALUES (%s, %s, %s, %s);
                ''',
                (transaction_info['transaction_id'],
                 item['item_id'], item['label'], item['quantity'])
            )

        return_data = transaction_info
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully created transaction', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def edit_transactions_status(transaction_id, status):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            UPDATE transactions
            SET status=%s
            WHERE transaction_id=%s;
            ''',
            (status, transaction_id)
        )

        return_data = connection_manager.get_data(cursor)
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully updated transactions status', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res


def get_teams_transactions(team_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM transactions
            WHERE team_id=%s;
            ''',
            (team_id,)
        )
        transactions = connection_manager.get_data(cursor, 'transactions')

        for transaction in transactions['transactions']:
            cursor.execute(
                '''
				SELECT transactionsitems.label, transactionsitems.quantity, items.item_id, items.name
                FROM transactionsitems
                INNER JOIN items
                USING (item_id)
                WHERE transaction_id=%s;
                ''',
                (transaction['transaction_id'],)
            )
            items = connection_manager.get_data(cursor, 'items')
            transaction.update(items)

        return_data = transactions
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved transactions', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res

def get_teams_transactions(transaction_id):
    try:
        connection = connection_manager.connect()
        cursor = connection.cursor()

        cursor.execute(
            '''
            SELECT *
            FROM transactions
            WHERE transaction_id=%s;
            ''',
            (transaction_id,)
        )

        return_data = connection_manager.get_data(cursor, 'transactions')
        cursor.close()
        connection_manager.disconnect(connection)

        res = ('successfully retrieved transaction', False, return_data)
        return res
    except Exception as e:
        cursor.close()
        connection_manager.disconnect(connection)
        res = (str(e), True, {})
        return res
