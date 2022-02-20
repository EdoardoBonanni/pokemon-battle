import uuid
import numpy as np

class Player:
    def __init__(self):
        self.uid = uuid.uuid4().fields[-1] # id univoco Player
        self.team = []

    def add_pokemon(self, pokemon):
        if len(self.team) < 6:
            if pokemon.name not in self.pokemon_names():
                self.team.append(pokemon)
                return True
        elif len(self.team) == 6:
            if pokemon.name not in self.pokemon_names():
                self.team.pop()
                self.team.append(pokemon)
                return True
        return False

    def remove(self, pokemon):
        if pokemon.name in self.pokemon_names():
            index = self.search_pokemon(pokemon)
            self.team.pop(index)
            return True
        return False

    def substitute_pokemon(self, index_pokemon_to_remove, pokemon_to_insert):
        if pokemon_to_insert.name not in self.pokemon_names():
            if index_pokemon_to_remove < len(self.team):
                self.team[index_pokemon_to_remove] = pokemon_to_insert
                return True
        return False

    def swap_position(self, index1, index2):
        self.team[index1], self.team[index2] = self.team[index2], self.team[index1]

    def search_pokemon_alive(self):
        for i in range(len(self.team)):
            if self.team[i].battleHP_actual > 0:
                return i
        return -1

    def pokemon_names(self):
        return [pokemon.name for pokemon in self.team]

    def search_pokemon(self, pokemon_to_remove):
        for i in range(len(self.team)):
            if self.team[i].name == pokemon_to_remove.name:
                return i
        return -1






