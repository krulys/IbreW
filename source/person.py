class Person:

    def __init__(self, displayName, team, favDrink, PMUDrink="N/A"):
        self._displayName = displayName
        self._name = displayName.lower()
        self._team = team
        self._favDrink = favDrink
        self._PMUDrink = PMUDrink

    def __eq__(self,other):
        if isinstance(other, Person):
            return self.displayName == other.displayName and self.name == other.name and self.team == other.team and self.favDrink == other.favDrink and self.PMUDrink == other.PMUDrink
        return False
    def setDisplayName(self, displayName):
        self._displayName = displayName

    def setName(self,newName):
        self._name = newName

    def getName(self):
        return self._name

    def getDisplayName(self):
        return self._displayName
    
    def setTeam(self, team):
        self._team = team
    
    def getTeam(self):
        return self._team
    
    def setFavoriteDrink(self, favDrink):
        self._favDrink=favDrink
    
    def getFavoriteDrink(self):
        return self._favDrink

    def setPickMeUpDrink(self, PMUDrink):
        self._PMUDrink = PMUDrink

    def getPickMeUpDrink(self):
        return self._PMUDrink
    
    name = property(getName, setName)
    displayName = property(getDisplayName, setDisplayName)
    team = property(getTeam,setTeam)
    favDrink = property(getFavoriteDrink,setFavoriteDrink)
    PMUDrink = property(getPickMeUpDrink,setPickMeUpDrink)