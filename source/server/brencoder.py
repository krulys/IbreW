from json import JSONEncoder
from source.person import Person
from source.drink import Drink
from source.brewRound import BrewRound
class Brencoder(JSONEncoder):
    def default(self,o):
        if isinstance(o, Person):
            return Brencoder.personEncoder(self,o)
        elif isinstance(o,Drink):
            return Brencoder.drinkEncoder(self,o)
        elif isinstance(o,BrewRound):
            return Brencoder.roundEncoder(self,o)
        return o.__dict__ 

    def personEncoder(self,person):
        return { "person_id" : person._person_id , "displayName" : person._displayName , "name" : person._name , "team" : person._team, "favDrink" : Brencoder.drinkEncoder(self,person._favDrink)}

    def drinkEncoder(self,drink):
        return { "drink_id" : drink._drink_id , "displayName" : drink._displayName , "drink_type" : drink._drink_type, "recipe": drink._recipe}

    def roundEncoder(self,round):
        return { "round_id" : round.roundID , "initiator" : round.initiator._person_id }
        