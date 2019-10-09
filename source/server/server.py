from flask import *
import os
from source.state import State
from source.person import Person
from source.drink import Drink
from source.brewRound import BrewRound
from source.order import Order
from source.tables import Tables
from source.server.brencoder import Brencoder

app = Flask(__name__)
state = State()

#FavIcon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#Graphical

@app.route('/round/id/<round_id>/show')
def show_orders_by_round(round_id):
    currOrders = []
    for order in state._orders:
        if order._round.roundID == int(round_id):
            currOrders.append(order)
    
    return render_template("show_orders.html", is_tryit_active = True, orders=currOrders, round_id = round_id)


@app.route('/round/id/<round_id>')
def orders_by_round(round_id):
    currRound = state.findRoundByID(round_id)
    if currRound != -1 :
        participants = Tables.findPeopleByTeam(currRound.initiator._team,state._people)
        return render_template("add_order.html",
                            is_tryit_active = True,
                            initiator_name = currRound._initiator._displayName,
                            teammates = participants, drinks = state._drinks,
                            round_id = round_id
                            )
    else:
        abort(404)

@app.route('/app')
def app_page():
    return render_template("app.html", is_tryit_active = True, people=state.getPeople())


@app.route('/data/manage')
def manage_data():
    return render_template("manage_data.html",
                            is_tryit_active = True,
                            people=sorted(state._people, key=lambda person: person._person_id),
                            drinks=sorted(state._drinks, key=lambda drink: drink._drink_id),
                            orders=sorted(state._orders, key=lambda order: order._order_id),
                            rounds=sorted(state._rounds, key=lambda bRound: bRound._roundID)
                            )

@app.route('/')
def index():
    return render_template("index.html", is_home_active = True)

@app.route('/download')
def download():
    return render_template("download.html", is_download_active = True)

@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    if request.method == "GET":
        return render_template('add_form.html', title="Create Form")

    elif request.method == "POST":
        person_name = request.form.get("person-name")
        person_team = request.form.get("person-team")

        return render_template("return_person_team.html", title="Posted", name=person_name, team=person_team)


#API
@app.route('/api/people', methods=['GET', 'POST', 'DELETE'])
def api_people():
    if request.method == "GET":
        people = state.getPeople()
        encoder = Brencoder()
        return jsonify([encoder.default(person) for person in people])
    elif request.method == "POST":
        person_id = 0
        try:
            person_id  = int(request.get_json()["person_id"])
        except:
            person_id = -1
            
        displayName = request.get_json()["displayName"]
        team = request.get_json()["team"]
        favDrinkID = int(request.get_json()["favDrink_id"])
        if favDrinkID == 0:
            favDrinkID = state.findPersonByID(person_id)._favDrink._drink_id
        drink = state.findDrinkByID(favDrinkID)
        newPerson = None
        if person_id:
            newPerson = Person(person_id,displayName,team,drink)
        else:
            newPerson = Person(-1,displayName,team,drink)
        state.savePersonToDB(newPerson)
        state.loadPeopleFromDB()
        return "Done",201
    elif request.method == "DELETE":
        person_id = 0
        try:
            person_id  = int(request.get_json()["person_id"])
        except:
            return "No valid person found",404
        state.deletePersonFromDB(person_id)
        state.loadObjectsFromDB()
        return "Done",200
    

@app.route('/api/drinks', methods=['GET', 'POST', 'DELETE'])
def api_drinks():
    if request.method == "GET":
        drinks = state.getDrinks()
        encoder = Brencoder()
        return jsonify([encoder.default(drink) for drink in drinks])
    elif request.method == "POST":
        drink_id = 0
        try:
            drink_id  = int(request.get_json()["drink_id"])
        except:
            drink_id = -1
        displayName = request.get_json()["displayName"]
        drink_type = request.get_json()["drink_type"]
        recipe = request.get_json()["recipe"]
        newDrink = Drink(drink_id,displayName,drink_type,recipe)
        state.saveDrinkToDB(newDrink)
        state.loadDrinksFromDB()
        return "Done",201
    elif request.method == "DELETE":
        drink_id = 0
        try:
            drink_id  = int(request.get_json()["drink_id"])
        except:
            return "No valid person found",404
        state.deleteDrinkFromDB(drink_id)
        state.loadObjectsFromDB()
        return "Done",200

@app.route('/api/rounds', methods=['GET', 'POST', 'DELETE'])
def api_rounds():
    if request.method == "GET":
        rounds = state.getRounds()
        encoder = Brencoder()
        return jsonify([encoder.default(bRound) for bRound in rounds])
    elif request.method == "POST":
        initiatorID = int(request.get_json()["initiator"])
        newID = state._rounds[-1]._roundID
        bRound = None
        for index, person in enumerate(state._people):
            if person._person_id == initiatorID:
                participants = Tables.findPeopleByTeam(person.team,state._people)
                bRound = BrewRound(newID,person,participants)
        state.saveRoundToDB(bRound)
        state.loadRoundFromDB()
        return str(newID),201
    elif request.method == "DELETE":
        round_id = 0
        try:
            round_id  = int(request.get_json()["round_id"])
        except:
            return "No valid person found",404
        state.deleteRoundFromDB(round_id)
        state.loadObjectsFromDB()
        return "Done",200

@app.route('/api/orders', methods=['GET', 'POST', 'DELETE'])
def api_orders():
    if request.method == "GET":
        orders = state.getOrders()
        encoder = Brencoder()
        return jsonify([encoder.default(order) for order in orders])
    elif request.method == "POST":
        order_id = -1
        person = None
        bRound = None
        drink = None
        try:
            order_id = int(request.get_json()["order_id"])
        except:
            pass
        try:
            person = state.findPersonByID(int(request.get_json()["person_id"]))
            bRound = state.findRoundByID(int(request.get_json()["round_id"]))
            if request.get_json()["favDrink"]:
                drink = state.findPersonByID(person._person_id)._favDrink
            else:
                drink = state.findDrinkByID(int(request.get_json()["drink_id"]))
        except:
            abort(400)
        newOrder = Order(order_id,bRound,person,drink)
        state.saveOrderToDB(newOrder)
        state.loadOrderFromDB()
        return "Done",201
    elif request.method == "DELETE":
        order_id = 0
        try:
            order_id  = int(request.get_json()["order_id"])
        except:
            return "No valid person found",404
        state.deleteOrderFromDB(order_id)
        state.loadObjectsFromDB()
        return "Done",200


if __name__ == '__main__':
    if state.loadObjectsFromDB() == 0:
        app.run("0.0.0.0",port=8082,debug=True)
    else:
        print("Can't connect to DB")