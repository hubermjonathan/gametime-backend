import psycopg2
import psycopg2.pool
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))


class ConnectionManager:
    def __init__(self):
        self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
            5,
            20,
            user=environ.get('DB_USERNAME'),
            password=environ.get('DB_PASSWORD'),
            host=environ.get('DB_URL'),
            port='5432',
            database=environ.get('DB_NAME')
        )

    def connect(self):
        connection = self.connection_pool.getconn()
        connection.autocommit = True
        return connection

    def disconnect(self, connection):
        self.connection_pool.putconn(connection)

    def get_data(self, cursor, key_name='results'):
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


connection_manager = ConnectionManager()
