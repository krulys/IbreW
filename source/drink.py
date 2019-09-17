class Drink:

    def __init__(self, displayName , name, drink_type, recipe="N/A"):
        self._name = name
        self._displayName = displayName
        self._drink_type = drink_type
        self._recipe = recipe

    def __eq__(self,other):
        if isinstance(other, Drink):
            return self.name == other.name and self._displayName == other.displayName and self._drink_type == other.drink_type and self._recipe == other.recipe
        return False

    def setName(self,name):
        self._name=name.lower()
    
    def getName(self):
        return self._name

    def getDisplayName(self):
        return self._displayName

    def setDisplayName(self,displayName):
        self._displayName = displayName

    def setType(self, drink_type):
        self._drink_type = drink_type
    
    def getType(self):
        return self._drink_type
    
    def setRecipe(self, recipe):
        self._recipe=recipe
    
    def getRecipe(self):
        return self._recipe

    displayName = property(getDisplayName, setDisplayName)
    name = property(getName,setName)
    drink_type = property(getType,setType)
    recipe = property(getRecipe,setRecipe)