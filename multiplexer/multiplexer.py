from typing import List, Dict
from flask import Flask, render_template, flash, request, redirect, url_for
import mysql.connector
import json
import os
from werkzeug.utils import secure_filename
from flask_session import Session

multiplexer = Flask(__name__)
sess = Session()
sess.init_app(multiplexer)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
multiplexer.config['UPLOAD_FOLDER'] = 'test'

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
            filename = secure_filename(file.filename)
            file.save(os.path.join(multiplexer.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('add_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
        
if __name__ == '__main__':
    multiplexer.secret_key = 'super secret key'
    multiplexer.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(multiplexer)
    multiplexer.run(host='0.0.0.0', port=5000, debug=True)
