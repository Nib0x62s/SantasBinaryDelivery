from .constants import SANTAS_INIT_MESSAGE
from .server import Server, RequestHandler


def main():
    server = Server(SantasRequestHandler, port=57777)
    server.start_server()


class SantasRequestHandler(RequestHandler):
    def __init__(self, handle):
        super().__init__(handle)

    def handle_requests(self):
        self.respond_init()
        while True:
            message = self._handle.recv(4029)
            if len(message) <= 0:
                self._handle.close()
                return

    def respond_init(self):
        self._handle.send(SANTAS_INIT_MESSAGE)
