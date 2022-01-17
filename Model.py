
class Model:
    def __init__(self):
        # Player me.
        self.me = None
        # Player enemy.
        self.enemy = None
        # Pokedex.
        self.pokedex = None
        # Moves.
        self.moves = None
        # Connection.

    def add_me(self, me):
        self.me = me

    def add_enemy(self, enemy):
        self.me = enemy

    def add_pokedex(self, pokedex):
        self.pokedex = pokedex

    def add_moves(self, moves):
        self.moves = moves