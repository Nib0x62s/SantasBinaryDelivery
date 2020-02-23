import threading
import socket


class Server:
    def __init__(self, address='0.0.0.0', port=None):
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__shutdown_server = threading.Event()

    def start_server(self):
        self.__shutdown_server.clear()
        self.server_bind()
        self.server_listen()
        while not self.__shutdown_server.is_set():
            try:
                handle, _ = self.socket.accept()
                request_handler = RequestHandler(handle)
            except socket.error:
                self.__shutdown_server.set()
                self.server_close()

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((self.address, self.port))

    def server_listen(self):
        self.socket.listen(5)

    def server_close(self):
        self.socket.close()


class RequestHandler:

    def __init__(self, handle):
        self._handle = handle
        self.init_message = """
        ==============================
               Default Response
        ==============================
        """

    def handle_requests(self):
        self.respond_init()
        while True:
            message = self._handle.recv(4029)
            print(message)

    def respond_init(self):
        self._handle.send(self.init_message)

