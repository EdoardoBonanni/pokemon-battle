from PyQt5.QtWidgets import QApplication
from choose_pokemon import choose_pokemon
import sys
from models.Model import Model


def main():
    app = QApplication(sys.argv)
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setStyle('Fusion')
    model = Model()
    choose_pokemon_window = choose_pokemon(model)
    choose_pokemon_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

