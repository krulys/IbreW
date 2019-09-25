from json import JSONEncoder
from source.person import Person
class Brencoder(JSONEncoder):
    def default(self,o):
        return o.__dict__ 

    def personEncoder(self,person):
        if isinstance(person, Person):
            return { "person_id" : person._person_id , "displayName" : person._displayName , "name" : person._name , "team" : person._team}
        return default(person)
        