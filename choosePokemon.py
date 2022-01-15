from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, QFileInfo
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QLabel
from init_window import Ui_MainWindow
from Pokedex import Pokedex
from PyQt5.QtGui import QMovie
import time


class choosePokemon(QMainWindow):
    def __init__(self):
        super(choosePokemon, self).__init__()
        # get the Ui_MainWindow.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.i = 0

        self.initUI()

        self.show()
        self.interaction()

    def interaction(self):
        self.ui.add_pokemon.clicked.connect(self.prova)
        self.ui.button_battle.clicked.connect(self.prova)


    def initUI(self):
        self.pokedex = Pokedex()
        self.pokedex.readCSVMoves("Pokemon Moves.csv")
        self.pokedex.readCSVPokemon("Kanto Pokemon Spreadsheet.csv")
        self.names = list(self.pokedex.listPokemon.keys())

        item_name = self.names[0]
        item = self.pokedex.listPokemon[item_name]

        # self.movie = QMovie('Sprites/' + item_name.lower() + '.gif')
        self.ui.pokemon_img.setPixmap(QtGui.QPixmap('img_pokemon_png/' + item_name.lower() + '.png'))
        # self.ui.pokemon_img.setScaledContents(True)
        # self.ui.pokemon_img.setMovie(self.movie)
        # self.movie.start()

        # Set values
        self.ui.tableWidget.item(0, 1).setText(item_name)
        self.ui.tableWidget.item(1, 1).setText(str(item.type1) + " " + str(item.type2))
        self.ui.tableWidget.item(2, 1).setText(str(item.move1.name) + ", " + str(item.move2.name) + ", " + str(item.move3.name) + ", " + str(item.move4.name))
        self.ui.tableWidget.item(3, 1).setText(str(item.hp))
        self.ui.tableWidget.item(4, 1).setText(str(item.atk))
        self.ui.tableWidget.item(5, 1).setText(str(item.defense))
        self.ui.tableWidget.item(6, 1).setText(str(item.spAtk))
        self.ui.tableWidget.item(7, 1).setText(str(item.spDef))
        self.ui.tableWidget.item(8, 1).setText(str(item.speed))
        self.ui.tableWidget.item(9, 1).setText(str(item.total))

    def prova(self):
        item_name = self.names[self.i]
        item = self.pokedex.listPokemon[item_name]

        # self.movie = QMovie('Sprites/' + item_name.lower() + '.gif')
        self.ui.pokemon_img.setPixmap(QtGui.QPixmap('img_pokemon_png/' + item_name.lower() + '.png'))
        # self.ui.pokemon_img.setScaledContents(True)
        # self.ui.pokemon_img.setMovie(self.movie)
        # self.movie.start()

        # Set values
        self.ui.tableWidget.item(0, 1).setText(item_name)
        self.ui.tableWidget.item(1, 1).setText(str(item.type1) + " " + str(item.type2))
        self.ui.tableWidget.item(2, 1).setText(str(item.move1.name) + ", " + str(item.move2.name) + ", " + str(item.move3.name) + ", " + str(item.move4.name))
        self.ui.tableWidget.item(3, 1).setText(str(item.hp))
        self.ui.tableWidget.item(4, 1).setText(str(item.atk))
        self.ui.tableWidget.item(5, 1).setText(str(item.defense))
        self.ui.tableWidget.item(6, 1).setText(str(item.spAtk))
        self.ui.tableWidget.item(7, 1).setText(str(item.spDef))
        self.ui.tableWidget.item(8, 1).setText(str(item.speed))
        self.ui.tableWidget.item(9, 1).setText(str(item.total))

        self.ui.tableWidget.update()
        self.ui.pokemon_img.update()
        self.i += 1
        print(self.i)


if __name__ == "__main__":
    import sys
    import qdarkstyle
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    choose_pokemon = choosePokemon()
    choose_pokemon.show()
    sys.exit(app.exec_())


