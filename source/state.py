import pickle
import curses
from ui import UI as UI
from person import Person
from drink import Drink
from tables import Tables as tables

class State:

    PEOPLE_FILE = "dbs/people.db"
    DRINKS_FILE = "dbs/drinks.db"

    _people = []
    _drinks = []

    def loadObjects(screen):
        State._people = State.loadObjectFromFile(screen,State.PEOPLE_FILE)
        State._drinks = State.loadObjectFromFile(screen,State.DRINKS_FILE)

    def loadObjectFromFile(screen, file):
        data = None
        try:
            pickle_in = open(file,"rb")
            data = pickle.load(pickle_in)
        except:
            screen.addstr(f"Cant load data from {file}\n")
            screen.getch()
            return -1
        finally:
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
        curses.nocbreak()
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
        State._people.append(Person(name,team,favDrink,PMUDrink))

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
            name = UI.cursedInput("Enter name of drink: ")
        if not drink_type:
            drink_type = UI.cursedInput("Enter type of drink: ")
        if not recipe:
            recipe = UI.cursedInput("Enter recipe of drink (keep it short):")
        _drinks.append(Drink(name,drink_type,recipe))

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