from source.state import State as state
import http.server
import socketserver
from source.server.IbreWHandler import IbreWHandler
PORT = 8080



if __name__ == "__main__":
    state.loadObjectsFromDB(None)
    PORT = 8080
    handler = IbreWHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
else:
    pass