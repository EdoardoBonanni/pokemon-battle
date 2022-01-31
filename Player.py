import uuid
import numpy as np

class Player:
    def __init__(self):
        self.uid = uuid.uuid4().fields[-1] # id univoco Player
        self.team = []

    def add_pokemon(self, pokemon):
        if len(self.team) < 6:
            if pokemon not in self.team:
                self.team.append(pokemon)
                return True
        elif len(self.team) == 6:
            if pokemon not in self.team:
                self.team.pop()
                self.team.append(pokemon)
                return True
        return False

    def remove(self, pokemon):
        if pokemon in self.team:
            self.team.remove(pokemon)
            return True
        return False

    def substitute_pokemon(self, index_pokemon_to_remove, pokemon_to_insert):
        if pokemon_to_insert not in self.team:
            if index_pokemon_to_remove < len(self.team):
                self.team[index_pokemon_to_remove] = pokemon_to_insert
                return True
        return False

    # def add_pokemon(self, pokemon):
    #     if len(self.team) < 6:
    #         self.team[pokemon.name.lower()] = pokemon
    #         return True
    #     elif len(self.team) == 6:
    #         if not self.team.get(pokemon.name.lower()):
    #             self.team.popitem()
    #             self.team[pokemon.name.lower()] = pokemon
    #             return True
    #     return False
    #
    # def remove(self, pokemon):
    #     if self.team.get(pokemon.name.lower()):
    #         self.team.pop(pokemon.name.lower())
    #         return True
    #     return False
    #
    # def substitute_pokemon(self, pokemon_to_remove, pokemon_to_insert):
    #     print()




