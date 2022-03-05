class Message:
    def __init__(self, id):
        self.p0_went = False
        self.p1_went = False
        self.ready = False
        self.data = [None, None]
        self.id = id

    def get_data(self, player):
        return self.data[player]

    def reset_data(self, player):
        self.data[player] = None

    def play(self, player, data):
        self.data[player] = data
        if player == 0:
            self.p0_went = True
        else:
            self.p1_went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p0_went and self.p1_went

    def reset_went(self):
        self.p0_went = False
        self.p1_went = False

    def reset(self):
        self.data[0] = None
        self.data[1] = None
        self.p0_went = False
        self.p1_went = False

    def check_data(self):
        if self.data[0] == None and self.data[1] == None:
            self.reset_went()