import time
import socketio
from file_multiplayer import FileSharing
from copy import deepcopy

def parse_command(command):
    # returns the function to call and the arguments
    if command['type'] == 'insertText':
        return FileSharing.put, (command['pos'] - 1, command['keyCode'])
    elif command['type'] == 'insertLineBreak':
        return FileSharing.put, (command['pos'] - 1, '\n')
    elif command['type'] == 'deleteContentBackward':
        return FileSharing.delete, (command['pos'], 1)
    elif command['type'] == 'deleteContentForward':
        return FileSharing.delete, (command['pos'], 1)
    else:
        raise Exception

class SocketServer(socketio.Namespace):
    def __init__(self, filename):
        self.filename = filename
        self.code = filename.split('/')[-1]
        self.namespace = '/' + filename.split('/')[-1]
        print(self.namespace)
        super(SocketServer, self).__init__(self.namespace)
        self.fs = FileSharing(filename)
        self.command_buffers = {}
        self.command_buffers_sentinel = {}
        self.clients = set()

    def on_connect(self, sid, environ):
        self.clients.add(sid)
        # add new buffer for the new client
        self.command_buffers[sid] = []
        self.command_buffers_sentinel[sid] = []
        self.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

    def on_disconnect(self, sid):
        print('disconnect ', sid)
        try:
            del self.command_buffers[sid]
            del self.command_buffers_sentinel[sid]
            self.clients.remove(sid)
            self.emit('my_response', {'data': 'Disconnected', 'count': 0}, room=sid)
        except:
            pass
    
    def on_input(self, sid, message):
        # handle the message
        self.command_buffers[sid].append(parse_command(message))
        return "OK", 123

    def file_jobs(self):
        # todo: use locking
        buffers = deepcopy(self.command_buffers)
        self.command_buffers = deepcopy(self.command_buffers_sentinel)

        for idx, buffer in buffers.items():
            # iterate through the command buffers
            for function, args in buffer:
                # iterate through each client's buffer and call the function
                function(self.fs, *args)
        
        # now send the updates to each client
        new_data = self.fs.get()
        self.emit('text_polling', {'all_text': new_data})

    def close(self):
        self.fs.close()

