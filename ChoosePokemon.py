from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import random
from UI.ChoosePokemonUI import Ui_MainWindow
from models.Pokedex import Pokedex
from models.Player import Player
from PyQt5.QtGui import QMovie
from UI.WidgetItemUI import Ui_widget_item
from functools import partial
from models.Model import Model
from GameModeSelection import GameModeSelection
from copy import deepcopy


class ChoosePokemon(QMainWindow):
    """
    ChoosePokemon class used to view all Pokemons with their stats and select a team to start the game.
    """
    def __init__(self, model: Model):
        super(ChoosePokemon, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = model
        self.names = None

        self.initUI()

        self.show()
        self.interaction()

    def initUI(self):
        """
        Initialize the window and every models.
        :return:
        """
        self.model.me = Player()
        self.model.enemy = Player()
        self.model.pokedex = Pokedex()
        self.names = list(self.model.pokedex.listPokemon.keys())

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

    def interaction(self):
        """
        Function that allow to interact with every element of the window.
        :return:
        """
        self.ui.add_pokemon.clicked.connect(self.add_pokemon_to_team)
        self.ui.remove_pokemon.clicked.connect(self.remove_pokemon_from_team)
        self.ui.list_item.itemClicked.connect(self.view_pokemon)
        self.ui.button_battle.clicked.connect(self.battle)
        self.ui.label_1.mouseDoubleClickEvent = partial(self.swap_pokemon, 1)
        self.ui.label_2.mouseDoubleClickEvent = partial(self.swap_pokemon, 2)
        self.ui.label_3.mouseDoubleClickEvent = partial(self.swap_pokemon, 3)
        self.ui.label_4.mouseDoubleClickEvent = partial(self.swap_pokemon, 4)
        self.ui.label_5.mouseDoubleClickEvent = partial(self.swap_pokemon, 5)
        self.ui.label_6.mouseDoubleClickEvent = partial(self.swap_pokemon, 6)

    def swap_pokemon(self, index, event):
        """
        Allow swapping Pokemon from the team to the new one that is selected from the list.
        :param index: Pokemon index in the team.
        :param event: Event.
        :return:
        """
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

    def update_stats(self, pokemon_item):
        """
        Update values in tableWidget.
        :param pokemon_item: Pokemon stats to visualize.
        :return:
        """
        self.ui.tableWidget.item(0, 1).setText(pokemon_item.name)
        self.ui.tableWidget.item(1, 1).setText(str(pokemon_item.type1) + " " + str(pokemon_item.type2))
        self.ui.tableWidget.item(2, 1).setText(str(pokemon_item.move1.name) + ", " + str(pokemon_item.move2.name) + ", " + str(pokemon_item.move3.name) + ", " + str(pokemon_item.move4.name))
        self.ui.tableWidget.item(3, 1).setText(str(int(pokemon_item.battleHP)))
        self.ui.tableWidget.item(4, 1).setText(str(int(pokemon_item.battleATK)))
        self.ui.tableWidget.item(5, 1).setText(str(int(pokemon_item.battleDEF)))
        self.ui.tableWidget.item(6, 1).setText(str(int(pokemon_item.battleSpATK)))
        self.ui.tableWidget.item(7, 1).setText(str(int(pokemon_item.battleSpDEF)))
        self.ui.tableWidget.item(8, 1).setText(str(int(pokemon_item.battleSpeed)))
        self.ui.tableWidget.item(9, 1).setText(str(int(pokemon_item.battleTotal)))

        self.ui.pokemon_img.setPixmap(QtGui.QPixmap('img_pokemon_png/' + pokemon_item.name.lower() + '.png'))  # Set pokemon_img pixmap.

    def view_pokemon(self):
        """
        Update Pokemon and stats in the window.
        :return:
        """
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        if item_name.lower() != self.ui.tableWidget.item(0, 1).text().lower():
            item = self.model.pokedex.listPokemon[item_name]
            self.update_stats(item)
        self.ui.tableWidget.show()
        self.ui.text_label.hide()

    def add_pokemon_to_team(self):
        """
        Add Pokemon into the team.
        :return:
        """
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        item = deepcopy(self.model.pokedex.listPokemon[item_name])
        if self.model.me.add_pokemon(item):
            self.update_team()

    def remove_pokemon_from_team(self):
        """
        Remove Pokemon from the team.
        :return:
        """
        pos = self.ui.list_item.currentRow()
        item_name = self.names[pos]
        item = deepcopy(self.model.pokedex.listPokemon[item_name])
        if self.model.me.remove(item):
            self.update_team()

    def update_team(self):
        """
        Update Pokemon gif in the team.
        :return:
        """
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
        """
        Choose Random Pokemon for testing.
        :return:
        """
        while len(self.model.me.team) < 6:
            index = random.randint(0, len(self.model.pokedex.listPokemon) - 1)
            pokemon = deepcopy(list(self.model.pokedex.listPokemon.values())[index])
            if pokemon.name not in self.model.me.pokemon_names():
                self.model.me.add_pokemon(pokemon)

    def battle(self):
        """
        Start the battle if the team is full, else warning message.
        :return:
        """
        self.choose_random_pokemon()
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Venusaur']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Dragonite']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Marowak']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Graveler']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Fearow']))
        # self.model.me.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Weezing']))
        if len(self.model.me.team) == 6:
            self.change_window = GameModeSelection(self.model, self, self.pos().x() + 15, self.pos().y() + 30)
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
    choose_pokemon = ChoosePokemon(model)
    choose_pokemon.show()
    sys.exit(app.exec_())


