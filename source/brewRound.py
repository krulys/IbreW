class BrewRound:

    def __init__(self, people, initiator, teamName=None):
        self._teamName = teamName
        self._people = people
        self._initiatior = initiator
    
    def getInitiator(self):
        return self._initiatior

    def setInitiator(self, initiator):
        self._initiatior = initiator

    def setRoundID(self,roundID):
        self._roundID=roundID
    
    def getRoundID(self):
        return self._roundID
    
    def setTeamName(self, teamName):
        self._teamName = teamName
    
    def getTeamName(self):
        return self._teamName
    
    def setPeople(self, people):
        self._people=people
    
    def getPeople(self):
        return self._people
    
    def addPerson(self,person):
        self._people.append(person)

    def start(self):
        # TODO Start round
        pass

    def stop(self):
        # TODO Stop round
        pass

    def display(self):
        # TODO Display all orders so far
        pass

    teamName = property(getTeamName,setTeamName)
    roundID = property(getRoundID,setRoundID)
    people = property(getPeople,setPeople)

