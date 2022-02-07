import uuid

class Pokemon:
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
        self.uid = uuid.uuid4().fields[-1] # id univoco Pokemon
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
        self.battleHP = int((self.hp + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 60) * 1.5)
        self.battleHP_actual = int((self.hp + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 60) * 1.5)
        self.battleATK = self.atk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleDEF = self.defense + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleSpATK = self.spAtk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleSpDEF = self.spDef + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleSpeed = self.speed + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.battleTotal = self.battleHP + self.battleATK + self.battleDEF + self.battleSpATK + self.battleSpDEF + self.battleSpeed

        # These variables are used to just hold the values of the original stat for stat modification purposes
        self.originalATK = self.atk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalDEF = self.defense + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalSpATK = self.spAtk + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalSpDEF = self.spDef + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5
        self.originalSpeed = self.speed + (0.5*Pokemon.IV) + (0.125*Pokemon.EV) + 5

        # In Battle Stats
        # Raised or lowered based on different moves used in battle. Affects the in battle stats (more info in the Overview of Battle Mechanics in readme.txt)
        self.atkStage = 0
        self.defStage = 0
        self.spAtkStage = 0
        self.spDefStage = 0
        self.speedStage = 0


    # Takes an int as input and returns a string with the pokemon losing that much HP
    def loseHP(self, lostHP):
        hp_actual = self.battleHP_actual
        self.battleHP_actual -= lostHP
        # Making sure battlHP doesn't fall below 0
        if self.battleHP_actual <= 0:
            self.battleHP_actual = 0
        return self.battleHP_actual - hp_actual

            # Takes an int as input and returns a string with the pokemon gaining that much HP
    def gainHP(self, gainedHP):
        hp_actual = self.battleHP_actual
        self.battleHP_actual += gainedHP
        if self.battleHP_actual > self.battleHP:
            self.battleHP_actual = self.battleHP
        return self.battleHP_actual - hp_actual

    # Determines if the Pokemon still has HP and returns a boolean
    def isAlive(self):
        if self.battleHP_actual > 0:
            return True
        else:
            return False

