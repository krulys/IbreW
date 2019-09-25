import pickle
import curses
import pymysql
import os
from source.ui import UI as UI
from source.person import Person
from source.drink import Drink
from source.tables import Tables as tables



class State:

    PEOPLE_FILE = "./dbs/people.db"
    DRINKS_FILE = "./dbs/drinks.db"

    _people = []
    _drinks = []

    def savePeopleToDB(screen):
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            for person in State._people:
                if person._person_id != -1:
                    cursor.execute("REPLACE INTO person(person_id, display_name , name , team , favDrink_id , PMUDrink_id) VALUES(%i ,%s , %s , %s , %i , %i);",(person._person_id ,person._displayName,person._name, person._favDrink._drink_id , person._PMUDrink._drink_id))
                else:
                    cursor.execute(f"INSERT INTO person(display_name , name , team , favDrink_id , PMUDrink_id ) VALUES({person._displayName} , {person._name}, {person._team},{person._favDrink._drink_id},{person._PMUDrink._drink_id});")
        except Exception as e:
            screen.clear()
            screen.addstr("Failed to save People\n")
            screen.addstr(str(e))
            screen.getch()


    def saveDrinksToDB(screen):
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            for drink in State._drinks:
                cursor.execute(f"REPLACE INTO drink(drink_id, display_name,drink_type,recipe)VALUES({drink._drink_id},{drink._displayName}, {drink._drink_type}, {drink._recipe});")

        except Exception as e:
            screen.clear()
            screen.addstr("Failed to save Drinks\n")
            screen.addstr(str(e))
            screen.getch()

    def saveObjectsToDB(screen):
        State.savePeopleToDB(screen)
        State.saveDrinksToDB()

    def loadDrinksromDB(screen):
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

            for row in results:
                drink_id = row[0]
                displayName = row[1]
                drink_type = row[2]
                recipe = row[3]
                State._drinks.append(Drink(drink_id,displayName,drink_type,recipe))
        except:
            print("Something went wrong with drinks...")

    def loadPeopleFromDB(screen):
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

            for row in results:
                person_id = row[0]
                displayName = row[1]
                name = row[2]
                team = row[3]
                favDrink = State._drinks[row[4]-1]
                if row[5] != "NULL":
                    PMUDrink = State._drinks[row[5]-1]
                else:
                    PMUDrink = None
                State._people.append(Person(person_id,displayName,team,favDrink,PMUDrink))


                print(f"{displayName}, {name}, {team}")
        except Exception as e:
            print(e)

    def loadObjectsFromDB(screen):
        State.loadDrinksromDB(screen)
        State.loadPeopleFromDB(screen)

    def loadObjects(screen):
        State._people = State.loadObjectFromFile(screen,State.PEOPLE_FILE)
        if State._people == -1 :
            State._people = []
        State._drinks = State.loadObjectFromFile(screen,State.DRINKS_FILE)
        if State._drinks == -1 :
            State._drinks = []

    def loadObjectFromFile(screen, file):
        data = None
        pickle_in = None
        try:
            pickle_in = open(file,"rb")
            data = pickle.load(pickle_in)
        except:
            screen.addstr(f"Cant load data from {file}\n")
            screen.getch()
            return -1
        finally:
            if pickle_in != None :
                pickle_in.close()
        return data

    def saveObjects(screen):
        State.saveObjectToFile(screen,State.PEOPLE_FILE,State._people)
        State.saveObjectToFile(screen,State.DRINKS_FILE,State._drinks)

    def saveObjectToFile(screen,file, data):
        try:
            pickleOut = open(file,"wb")
            pickle.dump(data,pickleOut)
        except:
            screen.addstr(f"Cant save data to {file}\n")
            screen.refresh()
            return -1
        finally:
            pickleOut.close()

    def addNewPerson(screen, name="",team="",favDrink=None,PMUDrink="N/A"):
        UI.clearScreen(screen)
        screen.keypad(False)
        curses.echo()
        if not name:
            name = UI.cursedInput(screen,"Enter name of person: ")
        if not team:
            team = UI.cursedInput(screen,"Enter name of team person is in: ")
        if not favDrink:
            if State._drinks != []:
                favDrink = tables.handleSingleSelectTable(
                    screen,"Drinks", State._drinks,"",0,
                    "Select this persons favorite drink")
            elif favDrink == None:
                UI.clearScreen(screen)
                screen.addstr("No drinks found. You can assign drink later...")
                screen.getch()
        State._people.append(Person(-1,name,team,favDrink,PMUDrink))

    def removePeople(screen):
        removableItems = tables.handleMultiSelectTable(screen,"People",State.getPeople(),"",0)
        for item in removableItems:
            State._people.remove(item)
    
    def getPeople():
        return State._people

    def sortPeople():
        State._people.sort()

    def reversePeople():
        State._people.reverse()


    def getDrinks():
        return State._drinks

    def sortDrinks():
        State._drinks.sort()

    def reverseDrinks():
        State._drinks.reverse()

    def addNewDrink(screen, name="",drink_type="",recipe=None):
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

    def removeDrinks(screen, removableItems = None):
        if not removableItems:
            removableItems = tables.handleMultiSelectTable(screen,"Drinks",State.getDrinks(),"",0)
        for item in removableItems:
            State._drinks.remove(item)


    def assignFavDrinkPreference(screen):
        person = tables.handleSingleSelectTable(screen,"People", State._people, "", 0,"Select a person to assign drink to")
        drink = tables.handleSingleSelectTable(screen,"Drinks", State._drinks, "", 0 , f"Select drink to assign to {person.displayName}")
        person.favDrink = drink

    def assignPickMeUpDrinkPreference(screen):
        person = tables.handleSingleSelectTable(screen,"People", State._people, "", 0,"Select a person to assign drink to")
        drink = tables.handleSingleSelectTable(screen,"Drinks", State._drinks, "", 0 , f"Select drink to assign to {person.displayName}")
        person.PMUDrink = drink