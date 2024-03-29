import json
import http.server
import os
from pathlib import Path
from source.state import State
from source.person import Person
from source.drink import Drink
from source.brewRound import BrewRound
from source.tables import Tables as tables
from source.server.brencoder import Brencoder
from source.server.routes.main import routes
from source.server.responses.templateHandler import TemplateHandler
from source.server.responses.badRequestHandler import BadRequestHandler


class IbreWHandler(http.server.BaseHTTPRequestHandler):

    def _set_headers(self,statuscode):
        self.send_response(statuscode)
        self.send_header("Content-Type","application/json")
        self.end_headers()

    def _serve_api(self,state,path_args):
        if path_args[0] == "people":
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            if len(path_args) == 2:
                if int(path_args[1]) <= len(state._people) and int(path_args[1]) > 0:
                    jd = json.dumps(state._people[int(int(path_args[1])-1)], cls=Brencoder)
                    self.wfile.write(jd.encode("utf-8"))
                else:
                    self.send_response(404)
                    self.send_header('Content-type','plain/text')
                    self.end_headers()
                    self.wfile.write(bytes("404 Not found", "UTF-8"))
                    self.respond()
            else:
                jd = json.dumps(state._people, cls=Brencoder)
                self.wfile.write(jd.encode("utf-8"))
        elif self.path == "/drinks":
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            jd = json.dumps(state._drinks, cls=Brencoder)
            self.wfile.write(jd.encode("utf-8"))
        elif self.path == "/round":
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            jd = json.dumps(state._rounds, cls=Brencoder)
            self.wfile.write(jd.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header('Content-type','plain/text')
            self.end_headers()
            self.wfile.write(bytes("404 Not found", "UTF-8"))

    def render_people(self,people):
        result = ""
        for person in people:
            result += f"<li>{person._displayName}</li>\n"
        return result

    def render_drinks(self,drinks):
        result = ""
        for drink in drinks:
            result += f"<li>{drink._displayName}</li>\n"
        return result

    def do_GET(self):
        print('GET request received')
        path_args= self.path.split("/")[1::]

        state = State()
        state.loadObjectsFromDB()

        print(self.headers.get("Content-Type"))

        if self.headers.get("Content-Type") == "application/json":
            self._serve_api(state,path_args)
        else:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
    <head>
        <title>IbreW</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">
    </head>
    <body>
            <h1 class = "title">STUFF</h1>
            <h2 class = "subtitle"> People </h2>
            <ul>"""
            html += self.render_people(state._people) + """
            </ul>
            <h2 class = "subtitle">Drinks</h2>
            <ul>"""
            html += self.render_drinks(state._drinks) + """
            </ul>
    </body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
        return

    def do_POST(self):
        print('POST request received')
        path_args= self.path.split("/")[1::]
        contentLength = int(self.headers["Content-Length"])
        data = json.loads(self.rfile.read(contentLength))
        state = State()
        state.loadObjectsFromDB()

        if path_args[0] == "people":
            personId = len(state._people)
            if "id" in data:
                personId = data["id"]
            favDrink = state._drinks[data["favDrink_id"]]
            person = Person(personId,data["displayName"],data["team"],favDrink)
            state._people.append(person)
            state.savePeopleToDB()
            self.send_response(201)
            self.end_headers()
        elif self.path == "/drinks":
            drinkID = len(state._drinks)
            if "id" in data:
                drinkID = data["id"]
            drink = Drink(drinkID,data["displayName"],data["drink_type"],data["recipe"])
            state._drinks.append(drink)
            state.savePeopleToDB()
            self.send_response(201)
            self.end_headers()
        elif self.path == "/round":
            roundId = len(state._rounds)
            if "id" in data:
                roundId = data["id"]
            initiator = state._people[data["initiator"]]
            brewRound = BrewRound(roundId,initiator,tables.findPeopleByTeam(initiator._team,state._people))
            state._rounds.append(brewRound)
            print(state._rounds)
            state.saveRoundsToDB()
            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type','plain/text')
            self.end_headers()
            self.wfile.write(bytes("404 Not found", "UTF-8"))
            self.respond()

        return