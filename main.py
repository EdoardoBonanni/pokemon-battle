from PyQt5.QtWidgets import QApplication
from ChoosePokemon import ChoosePokemon
from models.Model import Model
import sys


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    model = Model()  # the singleton model instance.
    choose_pokemon = ChoosePokemon(model)  # ChoosePokemon window to start the game.
    choose_pokemon.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

