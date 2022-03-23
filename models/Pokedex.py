from utility.utils import readCSV_moves, readCSV_Pokemon, read_type_advantages


class Pokedex:
    """
    Pokedex class used to keep lists of all Pokemon, moves and types advantages.
    """

    def __init__(self):
        self.listMoves = readCSV_moves("csv/Pokemon Moves.csv")  # List of all moves.
        self.listPokemon = readCSV_Pokemon(self.listMoves, "csv/Kanto Pokemon Spreadsheet.csv")  # List of all Pokemon.
        self.type_advantages = read_type_advantages("csv/Type Advantages.csv")  # Type Advantages for check effectiveness of moves on Pokemon.
