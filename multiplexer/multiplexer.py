from typing import List, Dict
from flask import Flask, render_template, flash, request, redirect, url_for, make_response
import mysql.connector
import json
import os
from werkzeug.utils import secure_filename
from flask_session import Session
import requests
import random
import os

multiplexer = Flask(__name__)
sess = Session()
sess.init_app(multiplexer)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', '.md', '.yml'}
multiplexer.config['UPLOAD_FOLDER'] = 'test'
DB_ADMIN_HOST = os.getenv('ADMIN_HOST')
DB_ADMIN_HOST = 'db_admin'
WORKER_HOST = 'worker'

def choose_best_server():
    # get it from db_interface
    post_r = requests.get(f'http://{DB_ADMIN_HOST}:5000/get_servers')
    all_servers = list(post_r.json())
    # todo: actually use the database
    return 'test'
    return random.choice(all_servers)

@multiplexer.route('/', methods=['GET', 'POST'])  
def default():
    return redirect('/upload')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@multiplexer.route('/upload', methods=['GET', 'POST'])
def add_file():
    if request.method == 'POST':
        if not os.path.exists(multiplexer.config['UPLOAD_FOLDER']):
            os.makedirs(multiplexer.config['UPLOAD_FOLDER'])
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # create the new session
            params = {'server_id': choose_best_server()}
            post_r = requests.post(f'http://{DB_ADMIN_HOST}:5000/create_sess', json=params)
            sess_id = post_r.json()

            # todo: assign a worker to this file 
            # currently just use the only server
            # add the file to the worker
            params = {'sess_id': sess_id}
            files={'file': (sess_id, file)}

            requests.post(f'http://{WORKER_HOST}:5000/upload_new', files=files)

            # set sess_id cookie and redirect
            actual_url = ':'.join(request.url.split(':')[:2])
            response = make_response(redirect(f'{actual_url}:5001/'))
            response.set_cookie('sess_id', sess_id)
            return response
            
    return render_template('index.html')
        
if __name__ == '__main__':
    multiplexer.secret_key = 'super secret key'
    multiplexer.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(multiplexer)
    multiplexer.run(host='0.0.0.0', port=5000, debug=True)
