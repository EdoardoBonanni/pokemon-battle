from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, QFileInfo
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QLabel
from view_choose_pokemon import Ui_MainWindow
from Pokedex import Pokedex
from Player import Player
from PyQt5.QtGui import QMovie
import time
from widget_item import Ui_widget_item


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

    def keyPressEvent(self, key_event):
        if key_event.key() == Qt.Key_Return:
            self.view_img()
        else:
            super().keyPressEvent(key_event)

    def update_stats(self, item):
        # Set values tableWidget
        self.ui.tableWidget.item(0, 1).setText(item.name)
        self.ui.tableWidget.item(1, 1).setText(str(item.type1) + " " + str(item.type2))
        self.ui.tableWidget.item(2, 1).setText(str(item.move1.name) + ", " + str(item.move2.name) + ", " + str(item.move3.name) + ", " + str(item.move4.name))
        self.ui.tableWidget.item(3, 1).setText(str(item.hp))
        self.ui.tableWidget.item(4, 1).setText(str(item.atk))
        self.ui.tableWidget.item(5, 1).setText(str(item.defense))
        self.ui.tableWidget.item(6, 1).setText(str(item.spAtk))
        self.ui.tableWidget.item(7, 1).setText(str(item.spDef))
        self.ui.tableWidget.item(8, 1).setText(str(item.speed))
        self.ui.tableWidget.item(9, 1).setText(str(item.total))

        # Set pixmap
        self.ui.pokemon_img.setPixmap(QtGui.QPixmap('img_pokemon_png/' + item.name.lower() + '.png'))

    def interaction(self):
        self.ui.add_pokemon.clicked.connect(self.add_pokemon_to_team)
        self.ui.remove_pokemon.clicked.connect(self.remove_pokemon_from_team)
        self.ui.list_item.itemClicked.connect(self.view_pokemon)
        self.ui.button_battle.itemClicked.connect(self.battle)

    def initUI(self):
        self.me = Player()
        self.enemy = Player()
        self.pokedex = Pokedex()
        self.pokedex.readCSVMoves("Pokemon Moves.csv")
        self.pokedex.readCSVPokemon("Kanto Pokemon Spreadsheet.csv")
        self.names = list(self.pokedex.listPokemon.keys())

        for pokemon_name in self.names:
            pokemon = self.pokedex.listPokemon[pokemon_name]

            item = QtWidgets.QListWidgetItem(pokemon_name)
            widget = QtWidgets.QWidget()

            widget_item = Ui_widget_item()
            widget_item.setupUi(widget)
            movie = QMovie('Sprites/' + pokemon_name.lower() + '.gif')
            widget_item.label_gif.setMovie(movie)
            movie.start()
            widget_item.label_name.setText(pokemon_name)
            item.setSizeHint(widget.size())
            self.ui.list_item.addItem(item)
            self.ui.list_item.setItemWidget(item, widget)

        self.ui.list_item.setCurrentRow(0)
        item_name = self.names[self.ui.list_item.currentRow()]
        item = self.pokedex.listPokemon[item_name]
        self.update_stats(item)

    def view_pokemon(self):
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        if item_name.lower() != self.ui.tableWidget.item(0, 1).text().lower():
            item = self.pokedex.listPokemon[item_name]
            self.update_stats(item)

    def add_pokemon_to_team(self):
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        item = self.pokedex.listPokemon[item_name]
        if self.me.add_pokemon(item):
            self.update_team()

    def remove_pokemon_from_team(self):
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        item = self.pokedex.listPokemon[item_name]
        if self.me.remove(item):
            self.update_team()

    def update_team(self):
        team = list(self.me.team.keys())
        self.ui.label_1.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_2.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_3.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_4.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_5.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_6.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        if 0 < len(team) <= 6:
            name = team[0]
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_1.setMovie(movie)
            movie.start()
        if 1 < len(team) <= 6:
            name = team[1]
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_2.setMovie(movie)
            movie.start()
        if 2 < len(team) <= 6:
            name = team[2]
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_3.setMovie(movie)
            movie.start()
        if 3 < len(team) <= 6:
            name = team[3]
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_4.setMovie(movie)
            movie.start()
        if 4 < len(team) <= 6:
            name = team[4]
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_5.setMovie(movie)
            movie.start()
        if len(team) == 6:
            name = team[5]
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_6.setMovie(movie)
            movie.start()

    def battle(self):
        team = self.me.team


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


