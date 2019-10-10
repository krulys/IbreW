import pickle
import curses
import pymysql
import os
import source.ui as UI
from source.person import Person
from source.drink import Drink
from source.brewRound import BrewRound
from source.order import Order
from source.tables import Tables as tables



class State:

    PEOPLE_FILE = "./dbs/people.db"
    DRINKS_FILE = "./dbs/drinks.db"

    _people = []
    _drinks = []
    _rounds = []

    def deletePersonFromDB(self, person_id):
        deleteSQL =  "DELETE FROM person WHERE person_id = %s;"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute(deleteSQL,(person_id))
            db.commit()
            cursor.close()
            
            return 0
        except Exception as e:
            print("Something went wrong")
            print(f"Error: {e}")
            return -1
        
    def deleteDrinkFromDB(self, drink_id):
        deleteSQL =  "DELETE FROM drink WHERE drink_id = %s;"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute(deleteSQL,(drink_id))
            db.commit()
            cursor.close()
            
            return 0
        except Exception as e:
            print("Something went wrong")
            print(f"Error: {e}")
            return -1
        
    def deleteRoundFromDB(self, round_id):
        deleteSQL =  "DELETE FROM round WHERE round_id = %s;"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute(deleteSQL,(round_id))
            db.commit()
            cursor.close()
            
            return 0
        except Exception as e:
            print("Something went wrong")
            print(f"Error: {e}")
            return -1
        
    def deleteOrderFromDB(self, order_id):
        deleteSQL =  "DELETE FROM brew_order WHERE order_id = %s;"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute(deleteSQL,(order_id))
            db.commit()
            cursor.close()
            
            return 0
        except Exception as e:
            print("Something went wrong")
            print(f"Error: {e}")
            return -1

    def saveOrdersToDB(self):
        insertSQL =  "INSERT INTO brew_order(round_id, person_id, drink_id)VALUES(%s,%s,%s);"
        replaceSQL = "REPLACE INTO brew_order (order_id, round_id, person_id, drink_id) VALUES(%s, %s, %s, %s)"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            for order in self._orders:
                if order.__order_id != -1:
                    result = cursor.execute(replaceSQL,
                    (order._order_id , order._round_id, order._person_id,order._drink_id )
                    )
                else:
                    result = cursor.execute(insertSQL,(order._round_id, order._person_id,order._drink_id))
            db.commit()
            cursor.close()
            
            return 0
        except Exception as e:
            print("Something went wrong")
            print(f"Error: {e}")
            return -1
    
    def saveOrderToDB(self,order):
        insertSQL =  "INSERT INTO brew_order(round_id, person_id, drink_id)VALUES(%s,%s,%s);"
        replaceSQL = "UPDATE brew_order SET round_id = %s, person_id = %s, drink_id = %s , favDrink_id =%s WHERE order_id = %s"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            if order._order_id != -1:
                result = cursor.execute(replaceSQL,
                (order._round._roundID, order._person._person_id, order._drink._drink_id, order._order_id  )
                )
            else:
                result = cursor.execute(insertSQL,(order._round._roundID, order._person._person_id ,order._drink._drink_id))
            db.commit()
            cursor.close()
            
            return 0
        except Exception as e:
            print("Something went wrong")
            print(f"Error: {e}")
            return -1

    def saveRoundsToDB(self):
        insertSQL =  "INSERT INTO round (initiator) VALUES(%s)"
        replaceSQL = "UPDATE round SET initiator = %s WHERE round_id = %s"
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
    def saveRoundToDB(self, brewRound):
        insertSQL =  "INSERT INTO round (round_id, initiator) VALUES(%s,%s)"
        replaceSQL = "UPDATE round SET initiator = %s WHERE round_id = %s"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            
            cursor.execute(insertSQL,
            (brewRound._roundID , brewRound._initiator._person_id)
            )
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
        
    def savePersonToDB(self,person):
        insertSQL =  "INSERT INTO `person` (display_name , name , team, favDrink_id ) VALUES(%s,%s,%s,%s)"
        replaceSQL = "UPDATE person SET display_name = %s, name = %s, team = %s , favDrink_id =%s WHERE person_id = %s"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            if person._person_id != -1:
                result = cursor.execute(replaceSQL,
                ( person._displayName , person._name,
                  person._team , person._favDrink._drink_id,
                  person._person_id))
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
        
    def saveDrinkToDB(self, drink):
        insertSQL =  "INSERT INTO drink (display_name , drink_type , recipe) VALUES(%s,%s,%s)"
        replaceSQL = "UPDATE drink SET display_name = %s, drink_type = %s, recipe = %s  WHERE drink_id = %s"
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            if drink._drink_id != -1:
                result = cursor.execute(replaceSQL,
                ( drink._displayName , drink._drink_type 
                , drink._recipe, drink._drink_id))
            else:
                result = cursor.execute(insertSQL,
                (drink._displayName , drink._drink_type 
                , drink._recipe))
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
                favDrink = self.findDrinkByID(row[4])
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
                initiator = self.findPersonByID(initiatorID)
                #TODO rework participants
                participants = tables.findPeopleByTeam(initiator._team,self._people)
                self._rounds.append(BrewRound(roundID,initiator,participants))
            cursor.close()
            return 0
        except Exception as e:
            print(f"Round Exception: {e}")
            return -1
        
    def loadOrderFromDB(self):
        try:
            db = pymysql.connect(
            os.environ["DB_HOST"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            "klaudijus"
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM brew_order")
            results = cursor.fetchall()
            self._orders = []
            for row in results:
                
                order_id = row[0]
                round_id = row[1]
                person_id = row[2]
                drink_id = row[3]
                
                self._orders.append(Order(order_id, self.findRoundByID(round_id), self.findPersonByID(person_id) ,self.findDrinkByID(drink_id)))
            cursor.close()
            return 0
        except Exception as e:
            print(f"Order Exception: {e}")
            return -1

    def loadObjectsFromDB(self):
        output = 0
        output += self.loadDrinksFromDB()
        output += self.loadPeopleFromDB()
        output += self.loadRoundFromDB()
        output += self.loadOrderFromDB()

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

    def getOrders(self):
        return self._orders

    def addNewDrink(self, screen=None, name=None, drink_type=None, recipe=None):
        if screen:
            UI.clearScreen(screen)
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
        if not name:
            name = UI.cursedInput(screen,"Enter name of drink: ")
        if not drink_type:
            drink_type = UI.cursedInput(screen,"Enter type of drink: ")
        if not recipe and recipe != "":
            recipe = UI.cursedInput(screen,"Enter recipe of drink (keep it short):")
        self._drinks.append(Drink(-1,name,drink_type,recipe))
        
        if screen:
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
        
    def findRoundByID(self,round_id):
        for round in self._rounds:
            if round._roundID == int(round_id):
                return round
            
        return -1
    
    def findPersonByID(self,person_id):
        for person in self._people:
            if person._person_id == int(person_id):
                return person
            
        return -1
    
    def findDrinkByID(self,drink_id):
        for drink in self._drinks:
            if drink._drink_id == int(drink_id):
                return drink
            
        return -1
    
    def findOrderByID(self,order_id):
        for order in self._orders:
            if order._order_id == int(order_id):
                return order
            
        return -1