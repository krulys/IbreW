from flask import *
from source.state import State
from source.person import Person
from source.drink import Drink
from source.brewRound import BrewRound
from source.tables import Tables
from source.server.brencoder import Brencoder

app = Flask(__name__)

def getNavBar():
    return """<header>
            <ul id="navbar">
                
                <li><a href="https://github.com/krulys/IbreW" class ="navbar-image-ref"><img id="nav-github-icon" src="https://img.icons8.com/color/48/000000/github--v1.png"/></a></li>
                <li><a href="#">Try it!</a></li>
                <li><a href="screenshots">Screenshots</a></li>
                <li><a href="/" class="active">Home</a></li>
            </ul>
        </header>"""

def getNavBarCSS():
    return f"<link rel='stylesheet' href= '{url_for('static', filename='css/navbar.css')}'>"

def getFontHead(font):
    if font.lower() == "roboto":
        return "<link href='https://fonts.googleapis.com/css?family=Roboto&display=swap' rel='stylesheet'>"

def wrapInBoilerplate(head,body):
    return f"""
<!DOCTYPE html>
<html>
{head}
{body}
</html>
"""

def generateHead(headEntries):
    html = """<head>
        <title>IbreW</title>"""
    for entry in headEntries:
        html += entry +"\n"
    html += "</head>"
    return html

def generateBody(body):
    return f"""<body>{body}</body>"""

#Graphical
@app.route('/')
def index():
    return render_template("actual_index.html", home_is_active=True)

@app.route('/people')
def people():
    state = State()
    state.loadPeopleFromDB()

    #HEAD
    headEntries = []

    #Font
    headEntries.append(getFontHead("roboto"))

    #CSS
    headEntries.append(getNavBarCSS())


    #Body
    body = ""
    body += getNavBar()

    #Content
    body+="<div id='content'>"
    peopleRows =""
    for person in state.getPeople():
        peopleRows += f"""
        <tr>
            <td>{person.displayName}</td>
            <td>{person.team}</td>
        </tr>"""

    body+=f"""
    <table>
        <caption><h2>People</h2></caption>
        <thead>
            <tr>
                <th>Name</th>
                <th>Team</th>
            </tr>
        </thead>
        <tbody>
            {peopleRows}
        </tbody>
    </table>"""
    body += "</div>"

    return wrapInBoilerplate(generateHead(headEntries),body)

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
        state = State()
        state.loadObjectsFromDB()

        people = state.getPeople()
        encoder = Brencoder()
        return jsonify([encoder.default(person) for person in people])
    elif request.method == "POST":
        displayName = request.get_json()["displayName"]
        team = request.get_json()["team"]
        favDrinkID = request.get_json()["favDrink_id"]

        state = State()
        state.loadDrinksFromDB()
        state.loadPeopleFromDB()
        drinks = state.getDrinks()

        newPerson = None
        for index, drink in enumerate(drinks):
            if drink._drink_id == favDrinkID:
                newPerson = Person(-1,displayName,team,drink)

        state._people.append(newPerson)
        state.savePeopleToDB()
        return "Done",201

@app.route('/api/drinks', methods=['GET', 'POST'])
def api_drinks():
    if request.method == "GET":
        state = State()
        state.loadDrinksFromDB()
        drinks = state.getDrinks()
        encoder = Brencoder()
        return jsonify([encoder.default(drink) for drink in drinks])
    elif request.method == "POST":
        displayName = request.get_json()["displayName"]
        drink_type = request.get_json()["drink_type"]
        recipe = request.get_json()["recipe"]

        state = State()
        state.loadDrinksFromDB()

        state._drinks.append(Drink(-1,displayName,drink_type,recipe))
        state.saveDrinksToDB()
        return "Done",201

@app.route('/api/rounds', methods=['GET', 'POST'])
def api_rounds():
    if request.method == "GET":
        state = State()
        state.loadObjectsFromDB()
        rounds = state.getRounds()
        encoder = Brencoder()
        return jsonify([encoder.default(bRound) for bRound in rounds])
    elif request.method == "POST":
        initiatorID = request.get_json()["initiator"]

        state = State()
        state.loadObjectsFromDB()
        print(f"Before: {len(state._rounds)}")
        for index, person in enumerate(state._people):
            if person._person_id == initiatorID:
                participants = Tables.findPeopleByTeam(person.team,state._people)
                state._rounds.append(BrewRound(-1,person,participants))
        print(f"After: {len(state._rounds)}")
        state.saveRoundsToDB()
        return "Done",201

if __name__ == '__main__':
   app.run("0.0.0.0",port=8081,debug=True)