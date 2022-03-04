class Message:
    def __init__(self, id):
        self.p1_went = False
        self.p2_went = False
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
            self.p1_went = True
        else:
            self.p2_went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1_went and self.p2_went

    def resetWent(self):
        # self.data[0] = None
        # self.data[1] = None
        self.p1_went = False
        self.p2_went = False