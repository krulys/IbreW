class Drink:

    def __init__(self, name, drink_type, recipe="N/A"):
        self.name = name
        self.drink_type = drink_type
        self.recipe = recipe

    def setName(self,name):
        self.displayName=name
        self.name=name.lower()
    
    def getName(self):
        return self.name

    def setType(self, drink_type):
        self.drink_type = drink_type
    
    def getType(self):
        return self.drink_type
    
    def setRecipe(self, recipe):
        self.recipe=recipe
    
    def getRecipe(self):
        return self.recipe
    
    name = property(getName,setName)
    drink_type = property(getType,setType)
    recipe = property(getRecipe,setRecipe)