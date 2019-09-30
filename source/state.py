import pickle
import curses
import pymysql
import os
import source.ui as UI
from source.person import Person
from source.drink import Drink
from source.brewRound import BrewRound
from source.tables import Tables as tables



class State:

    PEOPLE_FILE = "./dbs/people.db"
    DRINKS_FILE = "./dbs/drinks.db"

    _people = []
    _drinks = []
    _rounds = []

    def saveRoundsToDB(self):
        insertSQL =  "INSERT INTO round (initiator) VALUES(%s)"
        replaceSQL = "REPLACE INTO round (round_id, initiator) VALUES(%s, %s)"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            for brewRound in self._rounds:
                if brewRound._roundID != -1:
                    result = cursor.execute(replaceSQL,
                    (brewRound.roundID , brewRound.initiator._person_id )
                    )
                else:
                    result = cursor.execute(insertSQL,(brewRound.initiator._person_id))
            db.commit()
            cursor.close()
            
            return 0
        except Exception as e:
            print("Something went wrong")
            print(f"Error: {e}")
            return -1

    def savePeopleToDB(self):
        insertSQL =  "INSERT INTO `person` (display_name , name , team, favDrink_id ) VALUES(%s,%s,%s,%s)"
        replaceSQL = "REPLACE INTO person(person_id, display_name , name , team , favDrink_id ) VALUES(%s,%s,%s,%s,%s)"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            for person in self._people:
                if person._person_id != -1:
                    result = cursor.execute(replaceSQL,
                    (person._person_id , person._displayName , person._name 
                    , person._team , person._favDrink._drink_id))
                else:
                    result = cursor.execute(insertSQL,
                    (person._displayName,person._name, person._team,
                     person._favDrink._drink_id))
            db.commit()
            cursor.close()
            return 0
        except Exception as e:
            print(f"People saving exception: {e}")
            return -1
        
    def saveDrinksToDB(self):
        insertSQL =  "INSERT INTO drink (display_name , drink_type , recipe) VALUES(%s,%s,%s)"
        replaceSQL = "REPLACE INTO drink (drink_id, display_name , drink_type , recipe) VALUES(%s,%s,%s,%s)"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            for drink in self._drinks:
                if drink._drink_id != -1:
                    print("Replacing...")
                    result = cursor.execute(replaceSQL,
                    (drink._drink_id , drink._displayName , drink._drink_type 
                    , drink._recipe))
                    print(result)
                else:
                    print("Inserting...")
                    result = cursor.execute(insertSQL,
                    (drink._displayName , drink._drink_type 
                    , drink._recipe))
                    print(result)
            db.commit()
            cursor.close()
            return 0
        except Exception as e:
            print(f"Saving drinks exception: {e}")
            return -1

    def saveObjectsToDB(self):

        return State.savePeopleToDB(self) == 0 and State.saveDrinksToDB(self) == 0 and State.saveRoundsToDB(self)


    def loadDrinksFromDB(self):
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM drink")

            results = cursor.fetchall()
            self._drinks = []
            for row in results:
                drink_id = row[0]
                displayName = row[1]
                drink_type = row[2]
                recipe = row[3]
                self._drinks.append(Drink(drink_id,displayName,drink_type,recipe))
            cursor.close()
            return 0
        except Exception as e:
            print(f"Drinks Exception: {e}")
            return -1

    def loadPeopleFromDB(self):
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM person")

            results = cursor.fetchall()
            self._people = []
            for row in results:
                person_id = row[0]
                displayName = row[1]
                name = row[2]
                team = row[3]
                favDrink = None
                for drink in self._drinks:
                    if drink._drink_id == row[4]:
                        favDrink = drink
                        break
                self._people.append(Person(person_id,displayName,team,favDrink))
            cursor.close()
            db.close()
            return 0
        except Exception as e:
            print(f"People Exception: {e}")
            return -1

    def loadRoundFromDB(self):
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM round")
            results = cursor.fetchall()
            self._rounds = []
            for row in results:
                roundID = row[0]
                initiatorID = row[1]
                initiator = None
                for person in self._people:
                    if person._person_id == initiatorID:
                        initiator = person
                #TODO rework participants
                participants = tables.findPeopleByTeam(initiator._team,self._people)
                self._rounds.append(BrewRound(roundID,initiator,participants))
            cursor.close()
            return 0
        except Exception as e:
            print(f"Round Exception: {e}")
            return -1

    def loadObjectsFromDB(self):
        output = 0
        output += self.loadDrinksFromDB()
        output += self.loadPeopleFromDB()
        output += self.loadRoundFromDB()

        return output


    def addNewPerson(self,state,screen, name="",team="",favDrink=None):
        UI.clearScreen(screen)
        screen.keypad(False)
        curses.echo()
        if not name:
            name = UI.cursedInput(screen,"Enter name of person: ")
        if not team:
            team = UI.cursedInput(screen,"Enter name of team person is in: ")
        if not favDrink:
            if state._drinks != []:
                favDrink = tables.handleSingleSelectTable(
                    screen,"Drinks", state._drinks,"",0,
                    "Select this persons favorite drink")
            elif favDrink == None:
                UI.clearScreen(screen)
                screen.addstr("No drinks found. You can assign drink later...")
                screen.getch()
        state._people.append(Person(-1,name,team,favDrink))

    def removePeople(self,state,screen):
        removableItems = tables.handleMultiSelectTable(screen,"People",state._people,"",0)
        for item in removableItems:
            State._people.remove(item)
    
    def getPeople(self):
        return self._people

    def sortPeople(self):
        sorted(State._people, key=lambda person: person.displayName)

    def reversePeople(self):
        State._people.reverse()

    def getDrinks(self):
        return self._drinks

    def sortDrinks(self):
        sorted(State._drinks, key=lambda drink: drink.displayName)

    def reverseDrinks(self):
        State._drinks.reverse()

    def getRounds(self):
        return self._rounds

    def addNewDrink(self, screen, name="",drink_type="",recipe=None):
        UI.clearScreen(screen)
        
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()

        if not name:
            name = UI.cursedInput(screen,"Enter name of drink: ")
        if not drink_type:
            drink_type = UI.cursedInput(screen,"Enter type of drink: ")
        if not recipe:
            recipe = UI.cursedInput(screen,"Enter recipe of drink (keep it short):")
        State._drinks.append(Drink(name,drink_type,recipe))

        curses.cbreak()
        screen.keypad(True)
        curses.noecho()

    def removeDrinks(self, screen, removableItems = None):
        if not removableItems:
            removableItems = tables.handleMultiSelectTable(screen,"Drinks",State.getDrinks(),"",0)
        for item in removableItems:
            State._drinks.remove(item)


    def assignFavDrinkPreference(self,screen):
        person = tables.handleSingleSelectTable(screen,"People", State._people, "", 0,"Select a person to assign drink to")
        drink = tables.handleSingleSelectTable(screen,"Drinks", State._drinks, "", 0 , f"Select drink to assign to {person.displayName}")
        person.favDrink = drink