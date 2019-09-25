import json
import http.server
import os
from pathlib import Path
from source.state import State as state
from source.server.brencoder import Brencoder
from source.server.routes.main import routes
from source.server.responses.templateHandler import TemplateHandler
from source.server.responses.badRequestHandler import BadRequestHandler


class IbreWHandler(http.server.BaseHTTPRequestHandler):

    def _set_headers(self,statuscode):
        self.send_response(statuscode)
        self.send_header("Content-Type","application/json")
        self.end_headers()

    #def do_GET(self):
     #   split_path = os.path.splitext(self.path)
      #  request_extension = split_path[1]
       # print(self.path)
        #if request_extension is "" or request_extension is ".html":
         #   if self.path in routes:
          #      handler = TemplateHandler()
           #     handler.find(routes[self.path])
            #else:
             #   handler = BadRequestHandler()
#
 #       else:
  #          handler = BadRequestHandler()
#
 #       self.respond({
  #          'handler': handler
   #     })

    def do_GET(self):
        print   ('Get request received')
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        jd = json.dumps(state._people, cls=Brencoder)
        self.wfile.write(jd.encode("utf-8"))
        self.respond()
        return

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if status_code is 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        return bytes(content, 'UTF-8')

    def respond(self, handler):
        response = self.handle_http(handler['handler'])
        self.wfile.write(response)