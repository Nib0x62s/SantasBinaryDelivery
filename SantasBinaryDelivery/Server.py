import threading


class Server:
    def __init__(self, address='0.0.0.0', port=None):
        self.address = address
        self.port = port
        self.__shutdown_server = threading.Event()

    def start_server(self):
        while not self.__shutdown_server.is_set():
            pass
