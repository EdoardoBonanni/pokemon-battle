class Move:
    def __init__(self, id, name, description, type, kind, power, accuracy, pp):
        self.id = id  # Move's number id
        self.name = name  # Move's name

        # Description
        self.description = description  # Move description
        self.type = type  # Move type
        self.kind = kind  # Can be special, physical, or stat-changing

        # For in-battle calculations
        self.power = power  # Move's base damage
        self.accuracy = accuracy
        self.pp = pp

    # METHODS
    # str method
    def __str__(self):
        msg = self.name + " " + str(self.power)
        return msg

