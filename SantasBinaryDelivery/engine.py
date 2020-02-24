from .server import Server

def start_challenge():
    server = Server(port=57777)
    server.start_server()
