class Move(object):
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

    # GET Methods
    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getType(self):
        return self.type

    def getKind(self):
        return self.kind

    def getPower(self):
        return self.power

    def getAccuracy(self):
        return self.accuracy

    def getPP(self):
        return self.pp

    # SET Methods
    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setPower(self, power):
        self.power = power

    def setAccuracy(self, accuracy):
        self.accuracy = accuracy

    def setPP(self, pp):
        self.pp = pp
