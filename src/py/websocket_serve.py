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

class ClientInfo:
    def __init__(self):
        self.prev_message_time = datetime.now()
        self.prev_image_time = None

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('websocket.html')

class SocketHandler(websocket.WebSocketHandler):
    client_infos = defaultdict()

    def __init__(self, *args, **kwargs):
        super(SocketHandler, self).__init__(*args, **kwargs)
        servers = ['127.0.0.1:11211']
        self._mc = Client(servers)

    def open(self):
        self.client_infos[self] = ClientInfo()

    def on_close(self):
        del self.client_infos[self]

    def on_message(self, message):
        now = datetime.now()
        delta = now - self.client_infos[self].prev_message_time
        # TODO: Restrict access based on delta.

        time = self._mc.get('time')
        if self.client_infos[self].prev_image_time == time:
            self.write_message({'timeout': 50})
        else:
            image = self._mc.get('image')
            image = base64.b64encode(image)
            self.write_message({'image': image, 'timeout': 80})
            self.client_infos[self].prev_image_time = time
        self.client_infos[self].prev_message_time = now

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
