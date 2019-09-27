from source.state import State
import http.server
import socketserver
from source.server.IbreWHandler import IbreWHandler
PORT = 8080



if __name__ == "__main__":
    state = State()
    state.loadObjectsFromDB()
    PORT = 8080
    handler = IbreWHandler
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print("serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
else:
    pass