import uuid


class Player:
    """
    Player class used to keep its id, name and every method on its Pokemon team.
    """

    def __init__(self):
        self.uid = uuid.uuid4().fields[-1]  # unique id.
        self.name = None  # name.
        self.team = []  # Pokemon team.

    def add_pokemon(self, pokemon):
        """
        Add Pokemon into the team if it's not full or already present.
        :param pokemon: Pokemon to add in the team.
        :return: [True, False] if Pokemon is added or not.
        """
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

    def remove(self, pokemon_to_remove):
        """
        Remove Pokemon if exists in the team.
        :param pokemon_to_remove: Pokemon to remove in the team.
        :return: [True, False] if Pokemon is removed or not.
        """
        if pokemon_to_remove.name in self.pokemon_names():
            index = -1
            for i in range(len(self.team)):
                if self.team[i].name == pokemon_to_remove.name:
                    index = i
            if index != -1:
                self.team.pop(index)
                return True
        return False

    def substitute_pokemon(self, index_pokemon_to_remove, pokemon_to_insert):
        """
        Substitute Pokemon if exists in the team with another one.
        :param index_pokemon_to_remove: Index Pokemon to remove.
        :param pokemon_to_insert: Pokemon to add.
        :return: [True, False] if the new Pokemon is substituted or not.
        """
        if pokemon_to_insert.name not in self.pokemon_names():
            if index_pokemon_to_remove < len(self.team):
                self.team[index_pokemon_to_remove] = pokemon_to_insert
                return True
        return False

    def swap_position(self, index1, index2):
        """
        Swap position in the team between Pokemon.
        :param index1: First index Pokemon.
        :param index2: Second index Pokemon.
        :return:
        """
        self.team[index1], self.team[index2] = self.team[index2], self.team[index1]

    def search_pokemon_alive(self):
        """
        Check if a Pokemon in the team is alive.
        :return: [index, -1] Index of Pokemon alive else -1.
        """
        for i in range(len(self.team)):
            if self.team[i].battleHP_actual > 0:
                return i
        return -1

    def pokemon_names(self):
        """
        List of Pokemon name in the team.
        :return: List of Pokemon names
        """
        return [pokemon.name for pokemon in self.team]
