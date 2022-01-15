class Pokemon(object):
    # Values used to calculate Pokemon base stats
    IV = 30
    EV = 85
    STAB = 1.5  # Stands for "Same-type attack bonus"
    LEVEL = 100

    def __init__(self, id, name, type1, type2, hp, atk, defense, spAtk, spDef, speed, total, move1, move2, move3, move4):
        # da aggiungere move1, move2, move3, move4

        # ATTRIBUTES
        # Referring to the pokemonInfo list to fill in the rest of the attributes
        # ID Info
        self.id = id
        self.name = name
        self.level = Pokemon.LEVEL

        # Type
        self.type1 = type1
        self.type2 = type2

        # BASE STATS
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.spAtk = spAtk
        self.spDef = spDef
        self.speed = speed
        self.total = total

        # Moves
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4

        # In Battle Stats
        # The base stat is different from the in battle stat. The base stat is just used for calculating the in-battle stat
        # The in battle stats are calculated based on a formula from the games
        self.battleHP = int(self.hp + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 60)
        self.battleATK = self.atk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleDEF = self.defense + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleSpATK = self.spAtk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleSpDEF = self.spDef + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleSpeed = self.speed + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5

        # These variables are used to just hold the values of the original stat for stat modification purposes
        self.originalATK = self.atk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalDEF = self.defense + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalSpATK = self.spAtk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalSpDEF = self.spDef + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalSpeed = self.speed + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5

        # # Moves
        # # The Kanto Pokemon Spreadsheet has pre-determined movesets
        # self.move1 = Move(pokemonInfo[10])
        # self.move2 = Move(pokemonInfo[11])
        # self.move3 = Move(pokemonInfo[12])
        # self.move4 = Move(pokemonInfo[13])
        #
        # # A list containing all the moves; used for error-checking later
        # self.moveList = [self.move1.name.lower(), self.move2.name.lower(), self.move3.name.lower(), self.move4.name.lower()]

        # In Battle Stats
        # Raised or lowered based on different moves used in battle. Affects the in battle stats (more info in the Overview of Battle Mechanics in readme.txt)
        self.atkStage = 0
        self.defStage = 0
        self.spAtkStage = 0
        self.spDefStage = 0
        self.speedStage = 0

    # METHODS
    # Printing all the Pokemon info with the str method
    def __str__(self):
        msg = "Name: " + str(self.name) + "\nID: " + str(self.id) + "\nType1: " + str(self.type1) + \
              "\nType2: " + str(self.type2) + "\nBase HP: " + str(self.hp) + "\nBase ATK: " + str(self.atk) + "\nBase DEF: " + \
              str(self.defense) + "\nBase Sp. ATK: " + str(self.spAtk) + "\nBase Sp. DEF: " + str(self.spDef) + "\nBase Speed: " + str(self.speed)
        return msg

    # Get Attribute METHODS
    def getName(self):
        return self.name

    def getLevel(self):
        return self.level

    # Get BASE STAT METHODS
    def getHP(self):
        return self.hp

    def getATK(self):
        return self.atk

    def getDEF(self):
        return self.defense

    def getSpATK(self):
        return self.spAtk

    def getSpDEF(self):
        return self.spDef

    def getSpeed(self):
        return self.speed

    # Get STAT STAGE Methods
    def getAtkStage(self):
        return self.atkStage

    def getDefStage(self):
        return self.defStage

    def getSpAtkStage(self):
        return self.spAtkStage

    def getSpDefStage(self):
        return self.spDefStage

    def getSpeedStage(self):
        return self.speed

    # Set STAT STAGE Methods
    def setAtkStage(self, atkStage):
        self.atkStage = atkStage

    def setDefStage(self, defStage):
        self.defStage = defStage

    def setSpAtkStage(self, spAtkStage):
        self.spAtkStage = spAtkStage

    def setSpDefStage(self, spDefStage):
        self.spDefStage = spDefStage

    def setSpeedStage(self, speedStage):
        self.speedStage = speedStage

    # MOVE Methods
    def getMove1(self):
        return self.move1

    def getMove2(self):
        return self.move2

    def getMove3(self):
        return self.move3

    def getMove4(self):
        return self.move4

    def setMove1(self, move1):
        self.move1 = move1

    def setMove2(self, move2):
        self.move2 = move2

    def setMove3(self, move3):
        self.move3 = move3

    def setMove4(self, move4):
        self.move4 = move4

    # Print Methods
    # These methods return strings containing information about HP and movesets
    def printHP(self):
        msg = str(self.name) + ": HP " + str(self.battleHP)
        return msg

    def printMoves(self): # Take a list of move names as argument?
        msg = "\nMove 1: " + self.move1.moveInfo[1] + "\nMove 2: " + self.move2.moveInfo[1] + "\nMove 3: " + self.move3.moveInfo[1] + "\nMove 4: " + self.move4.moveInfo[1]
        return msg

    # In Battle Methods

    # Takes a move as input and returns a string with the pokemon using that move
    def useMove(self, move):
        msg = self.name + " used " + move.name + "!"
        return msg

    # Takes an int as input and returns a string with the pokemon losing that much HP
    def loseHP(self, lostHP):
        self.battleHP -= lostHP
        # Making sure battlHP doesn't fall below 0
        if self.battleHP <= 0:
            self.battleHP = 0
        msg = self.name + " lost " + str(lostHP) + " HP!"
        return msg

    # Takes an int as input and returns a string with the pokemon gaining that much HP
    def gainHP(self, gainedHP):
        self.hp += gainedHP

    # Determines if the Pokemon still has HP and returns a boolean
    def isAlive(self):
        if self.battleHP > 0:
            return True
        else:
            return False

    # If battleHP is 0, returns a string showing that the Pokemon fainted
    def faint(self):
        if self.battleHP <= 0:
            msg = self.name + " fainted "
            return msg
