import unittest
from unittest.mock import patch, Mock
from types import SimpleNamespace
from cursedIbreW import *

class unitTest_People(unittest.TestCase):
    def test_find_people_by_team(self):
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
        actual_output = findPeopleByTeam(initiator.team,testPeople)
        #Assert
        self.assertEqual(len(expected_output),len(actual_output))
        self.assertEqual(expected_output,actual_output)

    def test_create_person_1(self):
        #Arrange
        name = "Charlie"
        team = "Academy"
        drink = drinks[0]

        newPerson = Person(name, team, drink)
        test_people = getPeople().copy()
        test_people.append(newPerson)
        expected_output = test_people
        
        #Act
        addNewPerson(name, team, drink)
        actual_output = getPeople()
        #Assert
        self.assertEqual(len(actual_output),len(expected_output))
        self.assertEqual(expected_output,actual_output)
    def test_create_person_2(self):
        #Arrange
        name = "Edward ScissorHands The Barber of LongStringTown"
        team = "Academy"
        drink = drinks[0]


        newPerson = Person(name, team, drink)
        test_people = getPeople().copy()
        test_people.append(newPerson)
        expected_output = test_people
        
        #Act
        addNewPerson(name, team, drink)
        actual_output = getPeople()
        #Assert
        self.assertEqual(expected_output,actual_output)
    def test_create_person_empty(self):
        #Arrange
        name = " "
        team = " "
        drink = drinks[0]


        newPerson = Person(name, team, drink)
        test_people = getPeople().copy()
        test_people.append(newPerson)
        expected_output = test_people
        
        #Act
        addNewPerson(name, team, drink)
        actual_output = getPeople()
        #Assert
        self.assertEqual(expected_output,actual_output)
        
if __name__ == "__main__":
    unittest.main()