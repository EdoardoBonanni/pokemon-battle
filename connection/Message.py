class Message:
    """
    Message class to exchange messages/packets between client and server.
    """

    def __init__(self, id):
        self.p0_went = False  # Check if player 0 chose the move.
        self.p1_went = False  # Check if player 1 chose the move.
        self.data = [None, None]  # Packets of the two players.
        self.id = id  # Player id.

    def get_data(self, player):
        """
        Get data from the player.
        :param player: Player 0/1.
        :return: Return data from the player selected.
        """
        return self.data[player]

    def reset_data(self, player):
        """
        Reset data player.
        :param player: Player 0/1.
        :return:
        """
        self.data[player] = None

    def send_data(self, player, data):
        """
        Send data of the player and set True the sending variable.
        :param player: Player 0/1.
        :param data: Data message.
        :return:
        """
        self.data[player] = data
        if player == 0:
            self.p0_went = True
        else:
            self.p1_went = True

    def both_went(self):
        """
        Check if both players have done a move.
        :return: The sending variables of both players.
        """
        return self.p0_went and self.p1_went

    def reset_went(self):
        """
        Reset the sending variables to False.
        :return:
        """
        self.p0_went = False
        self.p1_went = False

    def check_data(self):
        """
        Check if data are None.
        :return:
        """
        if self.data[0] is None and self.data[1] is None:
            self.reset_went()
