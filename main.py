from PyQt5.QtWidgets import QApplication, QMainWindow
from choose_pokemon import choose_pokemon
import sys
import qdarkstyle
from Model import Model

#define font
# font = pygame.font.SysFont('Futura', 30)

#create screen fades
# intro_fade = ScreenFade(1, BLACK, 4)
# death_fade = ScreenFade(2, PINK, 4)


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

