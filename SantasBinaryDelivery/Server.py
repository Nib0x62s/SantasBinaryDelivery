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
        while not self.__shutdown_server.is_set():
            pass

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((self.address, self.port))
