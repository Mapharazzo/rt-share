import mysql.connector
import random
import sys
import string
from flask import Flask
from flask import request, jsonify, Response
import json

db_admin = Flask(__name__)

class DBWrapper():
    CONFIG = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
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
            except:
                # no connection available yet
                pass

    def get_all_servers(self):
        query = f"SELECT id FROM servers"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_session(self, server_id):
        # generate a random code for the new file
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=self.CODE_LEN))
            # check if the code exists in the database (low chance)
            query = f"SELECT * FROM sessions WHERE id='{code}'"
            self.cursor.execute(query)
            if len(self.cursor.fetchall()) == 0:
                break

        # now insert the new session into the database
        query = f"INSERT INTO sessions (id, server_id) VALUES ('{code}', '{server_id}')"

        return code

@db_admin.route('/create_sess', methods=['POST'])
def create_sess():
    global db
    params = request.get_json()
    server_id = params['server_id']
    sess_id = db.create_session(server_id)

    return jsonify(sess_id), 200

@db_admin.route('/get_servers', methods=['GET'])
def get_servers():
    global db
    print(db.get_all_servers())
    return jsonify(db.get_all_servers()), 200

if __name__ == '__main__':
    db = DBWrapper()

    db_admin.run(host='0.0.0.0')