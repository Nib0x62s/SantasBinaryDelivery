from .server import Server, RequestHandler


def start_challenge():
    server = Server(SantasRequestHandler, port=57777)
    server.start_server()


class SantasRequestHandler(RequestHandler):
    def __init__(self, handle):
        super().__init__(handle)

    def handle_requests(self):
        pass
