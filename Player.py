import uuid
import numpy as np

class Player:
    def __init__(self):
        self.uid = uuid.uuid4().fields[-1] # id univoco Player
        self.team = {}

    def add_pokemon(self, pokemon):
        if len(self.team) < 6:
            self.team[pokemon.name.lower()] = pokemon
            return True
        elif len(self.team) == 6:
            if not self.team.get(pokemon.name.lower()):
                self.team.popitem()
                self.team[pokemon.name.lower()] = pokemon
                return True
        return False

    def remove(self, pokemon):
        if self.team.get(pokemon.name.lower()):
            self.team.pop(pokemon.name.lower())
            return True
        return False

    # def substitute_pokemon(self, pokemon_to_remove, pokemon_to_insert):
    #     result = self.remove(pokemon_to_remove)
    #     if result:
    #         result = self.addPokemon(pokemon_to_insert)
    #     return result



