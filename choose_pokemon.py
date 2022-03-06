from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import random
from utility import utils
from UI.ChoosePokemonUI import Ui_MainWindow
from models.Pokedex import Pokedex
from models.Player import Player
from PyQt5.QtGui import QMovie
from UI.WidgetItemUI import Ui_widget_item
from functools import partial
from models.Model import Model
from start_battle_window import start_battle_window
from copy import deepcopy


class choose_pokemon(QMainWindow):
    def __init__(self, model: Model):
        super(choose_pokemon, self).__init__()
        # get the Ui_MainWindow.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = model
        self.names = None

        self.initUI()

        self.show()
        self.interaction()

    def interaction(self):
        self.ui.add_pokemon.clicked.connect(self.add_pokemon_to_team)
        self.ui.remove_pokemon.clicked.connect(self.remove_pokemon_from_team)
        self.ui.list_item.itemClicked.connect(self.view_pokemon)
        self.ui.button_battle.clicked.connect(self.battle)
        self.ui.label_1.mouseDoubleClickEvent = partial(self.substitute_pokemon, 1)
        self.ui.label_2.mouseDoubleClickEvent = partial(self.substitute_pokemon, 2)
        self.ui.label_3.mouseDoubleClickEvent = partial(self.substitute_pokemon, 3)
        self.ui.label_4.mouseDoubleClickEvent = partial(self.substitute_pokemon, 4)
        self.ui.label_5.mouseDoubleClickEvent = partial(self.substitute_pokemon, 5)
        self.ui.label_6.mouseDoubleClickEvent = partial(self.substitute_pokemon, 6)

    def initUI(self):
        self.model.me = Player()
        self.model.enemy = Player()
        self.model.pokedex = Pokedex()
        self.model.pokedex.readCSVMoves("csv/Pokemon Moves.csv")
        self.model.pokedex.readCSVPokemon("csv/Kanto Pokemon Spreadsheet.csv")
        self.names = list(self.model.pokedex.listPokemon.keys())
        self.model.type_advantages = utils.read_type_advantages("csv/Type Advantages.csv")

        for pokemon_name in self.names:
            item = QtWidgets.QListWidgetItem()
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

        # self.ui.list_item.setCurrentRow(0)
        # item_name = self.names[self.ui.list_item.currentRow()]
        # item = self.model.pokedex.listPokemon[item_name]
        # self.update_stats(item)

    def substitute_pokemon(self, index, event):
        pos = self.ui.list_item.currentRow()
        item_name_to_insert = self.names[pos]
        item_to_insert = self.model.pokedex.listPokemon[item_name_to_insert]
        if index == 1 and len(self.model.me.team) >= 1:
            if self.model.me.substitute_pokemon(0, item_to_insert):
                self.update_team()
        elif index == 2 and len(self.model.me.team) >= 2:
            if self.model.me.substitute_pokemon(1, item_to_insert):
                self.update_team()
        elif index == 3 and len(self.model.me.team) >= 3:
            if self.model.me.substitute_pokemon(2, item_to_insert):
                self.update_team()
        elif index == 4 and len(self.model.me.team) >= 4:
            if self.model.me.substitute_pokemon(3, item_to_insert):
                self.update_team()
        elif index == 5 and len(self.model.me.team) >= 5:
            if self.model.me.substitute_pokemon(4, item_to_insert):
                self.update_team()
        elif index == 6 and len(self.model.me.team) == 6:
            if self.model.me.substitute_pokemon(5, item_to_insert):
                self.update_team()

    def update_stats(self, item):
        # Set values tableWidget
        self.ui.tableWidget.item(0, 1).setText(item.name)
        self.ui.tableWidget.item(1, 1).setText(str(item.type1) + " " + str(item.type2))
        self.ui.tableWidget.item(2, 1).setText(str(item.move1.name) + ", " + str(item.move2.name) + ", " + str(item.move3.name) + ", " + str(item.move4.name))
        self.ui.tableWidget.item(3, 1).setText(str(int(item.battleHP)))
        self.ui.tableWidget.item(4, 1).setText(str(int(item.battleATK)))
        self.ui.tableWidget.item(5, 1).setText(str(int(item.battleDEF)))
        self.ui.tableWidget.item(6, 1).setText(str(int(item.battleSpATK)))
        self.ui.tableWidget.item(7, 1).setText(str(int(item.battleSpDEF)))
        self.ui.tableWidget.item(8, 1).setText(str(int(item.battleSpeed)))
        self.ui.tableWidget.item(9, 1).setText(str(int(item.battleTotal)))

        # Set pixmap
        self.ui.pokemon_img.setPixmap(QtGui.QPixmap('img_pokemon_png/' + item.name.lower() + '.png'))

    def view_pokemon(self):
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        if item_name.lower() != self.ui.tableWidget.item(0, 1).text().lower():
            item = self.model.pokedex.listPokemon[item_name]
            self.update_stats(item)
        self.ui.tableWidget.show()
        self.ui.text_label.hide()

    def add_pokemon_to_team(self):
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        item = deepcopy(self.model.pokedex.listPokemon[item_name])
        if self.model.me.add_pokemon(item):
            self.update_team()

    def remove_pokemon_from_team(self):
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        item = deepcopy(self.model.pokedex.listPokemon[item_name])
        if self.model.me.remove(item):
            self.update_team()

    def update_team(self):
        # team = list(self.me.team.keys())
        self.ui.label_1.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_2.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_3.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_4.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_5.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        self.ui.label_6.setPixmap(QtGui.QPixmap("img/pokeball.png"))
        if 0 < len(self.model.me.team) <= 6:
            name = self.model.me.team[0].name
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_1.setMovie(movie)
            movie.start()
        if 1 < len(self.model.me.team) <= 6:
            name = self.model.me.team[1].name
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_2.setMovie(movie)
            movie.start()
        if 2 < len(self.model.me.team) <= 6:
            name = self.model.me.team[2].name
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_3.setMovie(movie)
            movie.start()
        if 3 < len(self.model.me.team) <= 6:
            name = self.model.me.team[3].name
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_4.setMovie(movie)
            movie.start()
        if 4 < len(self.model.me.team) <= 6:
            name = self.model.me.team[4].name
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_5.setMovie(movie)
            movie.start()
        if len(self.model.me.team) == 6:
            name = self.model.me.team[5].name
            movie = QMovie('Sprites/' + name.lower() + '.gif')
            self.ui.label_6.setMovie(movie)
            movie.start()

    def choose_random_pokemon(self):
        while len(self.model.me.team) < 6:
            index = random.randint(0, len(self.model.pokedex.listPokemon) - 1)
            pokemon = deepcopy(list(self.model.pokedex.listPokemon.values())[index])
            if pokemon.name not in self.model.me.pokemon_names():
                self.model.me.add_pokemon(pokemon)

    def battle(self):
        # me
        self.choose_random_pokemon()
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Venusaur']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Gloom']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Marowak']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Abra']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Fearow']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Jolteon']))
        if len(self.model.me.team) == 6:
            self.change_window = start_battle_window(self.model, self, self.pos().x() + 15, self.pos().y() + 30)
            self.hide()
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle('Warning')
            msg_box.setWindowIcon(QtGui.QIcon('img/exclamation.png'))
            msg_box.setText("You have to choose 6 pokemon for the battle.")
            msg_box.exec_()



if __name__ == "__main__":
    import sys
    import qdarkstyle
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setStyle('Fusion')
    MainWindow = QtWidgets.QMainWindow()
    model = Model()
    choose_pokemon = choose_pokemon(model)
    choose_pokemon.show()
    sys.exit(app.exec_())


