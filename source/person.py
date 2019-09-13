class Person:

    def __init__(self, displayName, name,  team, favDrink, PMUDrink="N/A"):
        self._displayName = displayName
        self._name = name
        self._team = team
        self._favDrink = favDrink
        self._PMUDrink = PMUDrink

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

david = Person("David","david", "Academy", None)