import random


class Pokemon:
    """
    Pokemon class used to define all attributes, stats, moves and types for every Pokemon.
    """

    def __init__(self, id, name, type1, type2, hp, atk, defense, spAtk, spDef, speed, total, move1, move2, move3,
                 move4):
        # Values used to calculate Pokemon base stats.
        self.iv = 30  # Individual value Pokemon.
        self.ev = 85  # Effort value Pokemon.
        self.stab = 1.5  # Stands for "Same-type attack bonus".
        self.level = 100  # Pokemon level.

        # ATTRIBUTES.
        self.id = id  # Pokemon id.
        self.name = name  # Pokemon name.
        self.pokeball = random.randint(0, 3)  # Random Pokeball.

        # TYPE.
        self.type1 = type1  # Pokemon first type.
        self.type2 = type2  # Pokemon second type.

        # BASE STATS
        self.hp = hp  # Pokemon hp.
        self.atk = atk  # Pokemon attack.
        self.defense = defense  # Pokemon defense.
        self.spAtk = spAtk  # Pokemon special attack.
        self.spDef = spDef  # Pokemon special defense.
        self.speed = speed  # Pokemon speed.
        self.total = total  # Pokemon total stats.

        # Moves
        self.move1 = move1  # Pokemon move1.
        self.move2 = move2  # Pokemon move2.
        self.move3 = move3  # Pokemon move3.
        self.move4 = move4  # Pokemon move4.

        # In Battle Stats.
        # Base stats are different from Battle stats: the in battle stats are calculated based on a formula from the games.
        self.battleHP = int((self.hp + (0.5 * self.iv) + (0.125 * self.ev) + 60) * 1.5)
        self.battleHP_actual = int((self.hp + (0.5 * self.iv) + (0.125 * self.ev) + 60) * 1.5)
        self.battleATK = self.atk + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.battleDEF = self.defense + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.battleSpATK = self.spAtk + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.battleSpDEF = self.spDef + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.battleSpeed = self.speed + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.battleTotal = self.battleHP + self.battleATK + self.battleDEF + self.battleSpATK + self.battleSpDEF + self.battleSpeed

        # These variables are used to just hold the values of the original stat for stat modification purposes.
        self.originalATK = self.atk + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.originalDEF = self.defense + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.originalSpATK = self.spAtk + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.originalSpDEF = self.spDef + (0.5 * self.iv) + (0.125 * self.ev) + 5
        self.originalSpeed = self.speed + (0.5 * self.iv) + (0.125 * self.ev) + 5

        # In Battle Stats.
        # Raised or lowered based on different moves used in battle that affects the battle stats.
        self.atkStage = 0
        self.defStage = 0
        self.spAtkStage = 0
        self.spDefStage = 0
        self.speedStage = 0

    def loseHP(self, damage):
        """
        Decrease the Pokemon HP.
        :param damage: Damage dealt by a move.
        :return: HP that Pokemon lost.
        """
        hp_actual = self.battleHP_actual
        self.battleHP_actual -= damage
        # Making sure battlHP doesn't fall below 0.
        if self.battleHP_actual <= 0:
            self.battleHP_actual = 0
        return self.battleHP_actual - hp_actual

    def gainHP(self, gainedHP):
        """
        Increase the Pokemon HP.
        :param gainedHP: HP gained from a move.
        :return: HP that Pokemon gained.
        """
        hp_actual = self.battleHP_actual
        self.battleHP_actual += gainedHP
        if self.battleHP_actual > self.battleHP:
            self.battleHP_actual = self.battleHP
        return self.battleHP_actual - hp_actual
