"""
Serve webcam images from Memcached over a websocket.
"""

# Import standard modules.
import base64
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
    def __init__(self, *args, **kwargs):
        super(SocketHandler, self).__init__(*args, **kwargs)
        servers = ['127.0.0.1:11211']
        self._mc = Client(servers, debug=1)

    def on_message(self, message):
        value = self._mc.get('image')
        image = base64.b64encode(value)
        self.write_message(image)

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
