class Move:
    """
    Move class used to define all attributes of each move for every Pokemon.
    """

    def __init__(self, id, name, description, type, kind, power, accuracy, pp):
        self.id = id  # Move's number id.
        self.name = name  # Move's name.
        self.description = description  # Move's description.
        self.type = type  # Move's type.
        self.kind = kind  # Move's kind that can be special, physical, or stat-changing.

        # For in-battle calculations.
        self.power = power  # Move's base damage.
        self.accuracy = accuracy  # Move's accuracy.
        self.pp = pp  # Number of times that a move can be used.
        self.pp_remain = pp  # Number of times remained that a move can be used.