from Pokemon import Pokemon
from Move import Move

class Pokedex:
    def __init__(self):
        self.listPokemon = {}
        self.listMoves = {}

    def readCSVMoves(self, filename):
        fin = open(filename, 'r')
        for line in fin:
            line = line.strip()
            moveList = line.split(",")
            if any(map(str.isdigit, moveList[0])):
                id = moveList[0]
                name = moveList[1]
                description = moveList[2]
                type = moveList[3]
                kind = moveList[4]
                power = int(moveList[5])
                accuracy = moveList[6]
                pp = int(moveList[7])
                move = Move(id, name, description, type, kind, power, accuracy, pp)
                self.listMoves[name.lower()] = move  # Creating dicticionary with key = name and value is the move object
        fin.close()

    def readCSVPokemon(self, filename):
        fin = open(filename, 'r')
        for line in fin:
            line = line.strip()
            pokeList = line.split(",")
            if any(map(str.isdigit, pokeList[0])):
                id = pokeList[0]
                name = pokeList[1]
                type1 = pokeList[2]
                type2 = pokeList[3]
                hp = int(pokeList[4])
                atk = int(pokeList[5])
                defense = int(pokeList[6])
                spAtk = int(pokeList[7])
                spDef = int(pokeList[8])
                speed = int(pokeList[9])
                move1 = self.listMoves[pokeList[10].lower()]
                move2 = self.listMoves[pokeList[11].lower()]
                move3 = self.listMoves[pokeList[12].lower()]
                move4 = self.listMoves[pokeList[13].lower()]
                total = hp + atk + defense + spAtk + spDef + speed
                pokemon = Pokemon(id, name, type1, type2, hp, atk, defense, spAtk, spDef, speed, total, move1, move2, move3, move4)
                self.listPokemon[name] = pokemon  # Creating dicticionary with key = name and value is the pokemon object
        fin.close()

    def getListPokemon(self):
        for pokemon in self.listPokemon.values():
            print(pokemon.id, pokemon.name, pokemon.type1, pokemon.type2, pokemon.hp, pokemon.atk, pokemon.defense, pokemon.spAtk, pokemon.spDef, pokemon.speed,
                  pokemon.move1.name, pokemon.move2.name, pokemon.move3.name, pokemon.move4.name)



if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.readCSVMoves("Pokemon Moves.csv")
    pokedex.readCSVPokemon("Kanto Pokemon Spreadsheet.csv")
    pokedex.getListPokemon()
