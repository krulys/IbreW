class BrewRound:
    # TODO update to match new project structure
    def __init__(self, roundID, initiator, people):
        self._roundID = roundID
        self._initiator = initiator
        self._people = people
        self.updateDrinks()
    
    def getDrinks(self):
        return self._drinks
    
    def updateDrinks(self):
        favDrinks = []
        for member in self._people:
            favDrinks.append(member.favDrink)
        self._drinks = favDrinks

    def getInitiator(self):
        return self._initiator

    def setInitiator(self, initiator):
        self._initiator = initiator

    def setRoundID(self,roundID):
        self._roundID=roundID
    
    def getRoundID(self):
        return self._roundID
    
    def setPeople(self, people):
        self._people=people
    
    def getPeople(self):
        return self._people
    
    def addPerson(self,person):
        self._people.append(person)

    roundID = property(getRoundID,setRoundID)
    people = property(getPeople,setPeople)
    initiator = property(getInitiator,setInitiator)

