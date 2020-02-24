from .constants import INIT_MESSAGE

import logging
import socket
import threading


class Server:
    def __init__(self, handler_klass, address='0.0.0.0', port=None):
        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler_klass = handler_klass
        self.__shutdown_server = threading.Event()

    def start_server(self):
        self.__shutdown_server.clear()
        self.server_bind()
        self.server_listen()
        while not self.__shutdown_server.is_set():
            try:
                handle, _ = self.socket.accept()
                request_handler = self.handler_klass(handle)
                handler_thread = threading.Thread(target=request_handler.handle_requests, daemon=True)
                handler_thread.start()
            except socket.error:
                self.__shutdown_server.set()
                self.server_close()

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.address, self.port))

    def server_listen(self):
        self.socket.listen(5)

    def server_close(self):
        self.socket.close()


class RequestHandler:
    def __init__(self, handle):
        self._handle = handle
        self.init_message = INIT_MESSAGE

    def handle_requests(self):
        self.respond_init()
        while True:
            message = self._handle.recv(4029)
            if len(message) <= 0:
                self._handle.close()
                return
            print(message)

    def respond_init(self):
        self._handle.send(self.init_message)


