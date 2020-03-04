import mysql.connector
import random
import sys
import string

class DBWrapper():
    CONFIG = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': '32000',
        'database': 'rt_share'
    }

    CODE_LEN = 5

    def __init__(self):
        self.cursor = None
        counter = 0
        while not self.cursor:
            try:
                counter += 1
                if counter == 3:
                    sys.exit(0)
                self.connection = mysql.connector.connect(**self.CONFIG)
                self.cursor = self.connection.cursor()
            except mysql.connector.errors.DatabaseError:
                # no connection available yet
                pass

    def select_server(self):
        pass

    def create_session(self):
        # generate a random code for the new file
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=self.CODE_LEN))
            # check if the code exists in the database (low chance)
            self.cursor.execute(f'show tables')
            print(self.cursor.fetchall())
            query = f"SELECT * FROM sessions WHERE id='{code}'"
            self.cursor.execute(query)
            if len(self.cursor.fetchall()) == 0:
                break

        # now insert the new session into the database

        return 0

if __name__ == '__main__':
    db = DBWrapper()

    db.create_session()