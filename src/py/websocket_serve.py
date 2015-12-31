"""
Serve webcam images from Memcached over a websocket.
"""

# Import standard modules.
import base64
from datetime import datetime
from collections import defaultdict
import os
import sys

# Import 3rd-party modules.
from memcache import Client
from tornado import websocket, web, ioloop
import coils

port = int(sys.argv[1])

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('websocket.html')

class SocketHandler(websocket.WebSocketHandler):
    clients = defaultdict(str)

    def __init__(self, *args, **kwargs):
        super(SocketHandler, self).__init__(*args, **kwargs)
        servers = ['127.0.0.1:11211']
        self._mc = Client(servers, debug=1)

    def open(self):
        pass

    def on_message(self, message):
        time = self._mc.get('time')
        if self.clients[self] == time:
            self.write_message({'timeout': 50})
        else:
            image = self._mc.get('image')
            image = base64.b64encode(image)
            self.write_message({'image': image, 'timeout': 80})
            self.clients[self] = time

    def on_close(self):
        del self.clients[self]

template_folder = os.path.normpath(os.path.join(os.getcwd(), 'templates'))
static_folder = os.path.normpath(os.path.join(os.getcwd(), 'static'))
app = web.Application(
    [(r'/', IndexHandler),
     (r'/ws', SocketHandler)],
    template_path=template_folder,
    static_path=static_folder,
)

if __name__ == '__main__':
    app.listen(port)
    ioloop.IOLoop.instance().start()
