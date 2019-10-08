from flask import *
import os
from source.state import State
from source.person import Person
from source.drink import Drink
from source.brewRound import BrewRound
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
    state = State()
    state.loadObjectsFromDB()
    currRound = None
    #Get specified round
    for bRound in state._rounds:
        if bRound._roundID == int(round_id):
            currRound = bRound
            break
    print(currRound)
    print(currRound.initiator)
    participants = Tables.findPeopleByTeam(currRound.initiator._team,state._people)

    return render_template("add_order.html", is_tryit_active = True, initiator_name = currRound._initiator._displayName, teammates = participants, drinks = state._drinks)


@app.route('/round/id/<round_id>')
def orders_by_round(round_id):
    currRound = state.findRoundByID(round_id)
    #Get specified round

    participants = Tables.findPeopleByTeam(currRound.initiator._team,state._people)

    return render_template("add_order.html", is_tryit_active = True, initiator_name = currRound._initiator._displayName, teammates = participants, drinks = state._drinks)

@app.route('/app')
def app_page():
    return render_template("app.html", is_tryit_active = True, people=state.getPeople())

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
@app.route('/api/people', methods=['GET', 'POST'])
def api_people():
    if request.method == "GET":
        people = state.getPeople()
        encoder = Brencoder()
        return jsonify([encoder.default(person) for person in people])
    elif request.method == "POST":
        displayName = request.get_json()["displayName"]
        team = request.get_json()["team"]
        favDrinkID = request.get_json()["favDrink_id"]
        
        drinks = state.getDrinks()

        newPerson = None
        for index, drink in enumerate(drinks):
            if drink._drink_id == favDrinkID:
                newPerson = Person(-1,displayName,team,drink)

        state._people.append(newPerson)
        state.savePeopleToDB()
        state.loadPeopleFromDB()
        return "Done",201

@app.route('/api/drinks', methods=['GET', 'POST'])
def api_drinks():
    if request.method == "GET":
        drinks = state.getDrinks()
        encoder = Brencoder()
        return jsonify([encoder.default(drink) for drink in drinks])
    elif request.method == "POST":
        displayName = request.get_json()["displayName"]
        drink_type = request.get_json()["drink_type"]
        recipe = request.get_json()["recipe"]
        
        state._drinks.append(Drink(-1,displayName,drink_type,recipe))
        state.saveDrinksToDB()
        state.loadDrinksFromDB()
        return "Done",201

@app.route('/api/rounds', methods=['GET', 'POST'])
def api_rounds():
    if request.method == "GET":
        rounds = state.getRounds()
        encoder = Brencoder()
        return jsonify([encoder.default(bRound) for bRound in rounds])
    elif request.method == "POST":
        initiatorID = int(request.get_json()["initiator"])
        newID = state._rounds[-1]._roundID
        for index, person in enumerate(state._people):
            if person._person_id == initiatorID:
                participants = Tables.findPeopleByTeam(person.team,state._people)
                state._rounds.append(BrewRound(newID,person,participants))
        state.saveRoundsToDB()
        state.loadRoundFromDB()
        return str(newID),201

@app.route('/api/orders', methods=['GET', 'POST'])
def api_orders():
    if request.method == "GET":
        orders = state.getOrders()
        encoder = Brencoder()
        return jsonify([encoder.default(order) for order in orders])
    elif request.method == "POST":
        order_id = int(request.get_json()["order_id"])
        person_id = int(request.get_json()["person_id"])
        round_id = int(request.get_json()["round_id"])
        drink_id = int(request.get_json()["drink_id"])
        newID = state._orders[-1]._order_id
        state.saveRoundsToDB()
        state.loadRoundFromDB()
        return str(newID),201


if __name__ == '__main__':
    if state.loadObjectsFromDB() == 0:
        app.run("0.0.0.0",port=8082,debug=True)
    else:
        print("Can't connect to DB")