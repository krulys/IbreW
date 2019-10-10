import unittest
from unittest.mock import patch, Mock
from types import SimpleNamespace

from source.cursedIbreW import *
from source.person import Person
from source.drink import Drink
from source.tables import Tables as tables
from source.state import State
import source.ui as UI

class test_People(unittest.TestCase):

    def test_find_people_by_team(self):
        screen = initializeScreen()

        #Arrange
        initiator = Mock(Person)
        initiator.team = "Academy"

        member1 = Mock(Person)
        member1.team= "Academy"

        member2 = Mock(Person)
        member2.team = "Academy"

        member3 = Mock(Person)
        member3.team = "Hermes"

        member4 = Mock(Person)
        member4.team = "Sainsburys Bank"

        testPeople = [initiator, member1, member2, member3, member4]
        expected_output = [initiator, member1, member2]

        #Act
        actual_output = tables.findPeopleByTeam(initiator.team, testPeople)

        #Assert
        self.assertEqual(len(expected_output), len(actual_output))
        self.assertEqual(expected_output, actual_output)

        deinitializeScreen(screen)

    def test_calc_table_width(self):
        #Arrange
        title = "Testing"
        dataList = []
        obj = SimpleNamespace(displayName='Short')
        dataList.append(obj)
        obj = SimpleNamespace(displayName='Medium')
        dataList.append(obj)
        obj = SimpleNamespace(displayName='Longgggg')
        dataList.append(obj)
        obj = SimpleNamespace(displayName='VEEEEEEEERRRRRRYYYYYYY LOOOOOOOOOOONNNNNGGGGGGG')
        dataList.append(obj)
        expected_output = len(dataList[3].displayName)

        #Act
        actual_output = UI.calcTableWidth(title, dataList)

        #Assert
        self.assertEqual(expected_output, actual_output)
        
    def test_filter_table_1(self):
        #Arrange
        obj1 = SimpleNamespace(displayName='David')
        obj2 = SimpleNamespace(displayName='Dave')
        obj3 = SimpleNamespace(displayName='Henry')
        test_peeps = [obj1, obj2, obj3]
        #Act
        filtered_peeps = tables.filterTable(test_peeps, "D")
        #Assert
        self.assertEqual(2, len(filtered_peeps))

    def test_drink_member_variables_are_assigned_correctly(self):
        screen = initializeScreen()
        #Arrange
        state = State()
        displayName = "Coffee"
        drink_type = "coffee"
        recipe = ""
        #Act
        state.addNewDrink(None,displayName,drink_type,recipe)
        newDrink = state.getDrinks()[0]
        #Assert
        self.assertEqual(newDrink.displayName,displayName)
        self.assertEqual(newDrink.drink_type,drink_type)
        self.assertEqual(newDrink.recipe,recipe)

        #deinitializeScreen()

    def test_person_member_variables_are_assigned_correctly(self):
        screen = initializeScreen()
        state = State()
        #Arrange
        name = "Testing Test"
        team = "Test"
        favDrink = Mock(Drink)
        favDrink.drink_id = 1
        favDrink.displayName = "Coffee"
        favDrink.drink_type = "coffee"
        favDrink.recipe = None
        #Act
        state.addNewPerson(state,screen,name,team,favDrink)
        newPerson = state.getPeople()[0]
        #Assert
        self.assertEqual(len(state.getPeople()),1)
        self.assertEqual(newPerson.displayName, name)
        self.assertEqual(newPerson.name, name.lower())
        self.assertEqual(newPerson.team, team)
        self.assertEqual(newPerson.favDrink,favDrink)
        deinitializeScreen(screen)


if __name__ == "__main__":
    unittest.main()