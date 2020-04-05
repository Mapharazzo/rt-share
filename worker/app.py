import threading
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template, request, Response, redirect
from server import SocketServer
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
SCHED_TIME = 1
rooms = set()
app.config['UPLOAD_FOLDER'] = '/usr/src/app/files'

@app.route('/', methods=['GET', 'POST'])
def index():
    global sio
    # get the sess_id cookie if set
    sess_id = request.cookies.get('sess_id')
    if sess_id is None:
        sess_id = request.args.get('sess_id')
    if sess_id is None:
        return Response(status=404)

    return render_template('index.html', sess_id=sess_id)
    
@app.route('/upload_new', methods=['POST'])
def upload():
    # params = request.get_json()
    # filename = params['sess_id']
    file = request.files['file']
    filename = file.filename
    print(file)

    # file.save(filename)
    print(os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # server = SocketServer(filename)
    server = SocketServer(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    sio.register_namespace(server)
    background_thread = lambda: do_background(sio, server)
    thread = sio.start_background_task(background_thread)

    return Response(status=200)
   
def do_background(sio, server):
    while True:
        sio.sleep(SCHED_TIME)
        server.file_jobs()

if __name__ == '__main__':
    async_mode = 'threading'
    sio = socketio.Server(logger=True, async_mode=async_mode)

    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    print('a')

    app.run(host='0.0.0.0', threaded=True, debug=True, port=5000)
    # eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
