import time
import mysql.connector


def db_connector(config):
    from mysql.connector import errorcode

    for attempt in range(5):
        print(f"attemp=> {attempt}")
        try:
            _db_connection = mysql.connector.connect(**config)
            db_cursor = _db_connection.cursor()

            print("connection established")

            return {'connection': _db_connection, 'cursor': db_cursor}

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

            print(f"Error found. Sleep for 10 Sec")
            time.sleep(10)

    raise Exception('Database connection was not successful.')
