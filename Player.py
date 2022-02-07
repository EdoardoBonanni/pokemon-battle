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

    def swap_position(self, index1, index2):
        self.team[index1], self.team[index2] = self.team[index2], self.team[index1]

    def search_pokemon_alive(self):
        for i in range(len(self.team)):
            if self.team[i].battleHP_actual > 0:
                return i
        return -1






