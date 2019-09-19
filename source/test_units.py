import unittest
from unittest.mock import patch, Mock
from types import SimpleNamespace
from cursedIbreW import *
from person import Person
from tables import Tables as tables
from state import State as state
from ui import UI as UI
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

        testPeople = [initiator,member1,member2,member3,member4]
        expected_output = [initiator,member1,member2]
        #Act
        actual_output = tables.findPeopleByTeam(initiator.team,testPeople)
        #Assert
        self.assertEqual(len(expected_output),len(actual_output))
        self.assertEqual(expected_output,actual_output)
        deinitializeScreen()
    def test_create_person_1(self):
        screen = initializeScreen()
        #Arrange
        name = "Charlie"
        team = "Academy"
        drink = state.getDrinks()[0]

        newPerson = Person(name, team, drink)
        test_people = state.getPeople().copy()
        test_people.append(newPerson)
        expected_output = test_people
        
        #Act
        state.addNewPerson(screen,name, team, drink)
        actual_output = state.getPeople()
        #Assert
        self.assertEqual(len(actual_output),len(expected_output))
        self.assertEqual(expected_output,actual_output)
        deinitializeScreen()
    def test_create_person_2(self):
        screen = initializeScreen()
        #Arrange
        name = "Edward ScissorHands The Barber of LongStringTown"
        team = "Academy"
        drink = state.getDrinks()[0]


        newPerson = Person(name, team, drink)
        test_people = state.getPeople().copy()
        test_people.append(newPerson)
        expected_output = test_people
        
        #Act
        state.addNewPerson(screen,name, team, drink)
        actual_output = state.getPeople()
        #Assert
        self.assertEqual(expected_output,actual_output)
        deinitializeScreen()
    def test_create_person_empty(self):
        screen = initializeScreen()
        #Arrange
        name = " "
        team = " "
        drink = state.getDrinks()[0]


        newPerson = Person(name, team, drink)
        test_people = state.getPeople().copy()
        test_people.append(newPerson)
        expected_output = test_people
        
        #Act
        state.addNewPerson(screen,name, team, drink)
        actual_output = state.getPeople()
        #Assert
        self.assertEqual(expected_output,actual_output)
        deinitializeScreen()
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
        actual_output = UI.calcTableWidth(title,dataList)
        #Assert
        self.assertEqual(expected_output,actual_output)
        
    def test_filter_table_1(self):
        #Arrange
        obj1 = SimpleNamespace(displayName='David')
        obj2 = SimpleNamespace(displayName='Dave')
        obj3 = SimpleNamespace(displayName='Henry')
        test_peeps = [obj1,obj2,obj3]
        #Act
        filtered_peeps = tables.filterTable(test_peeps,"D")
        #Assert
        self.assertEqual(2,len(filtered_peeps))
if __name__ == "__main__":
    unittest.main()