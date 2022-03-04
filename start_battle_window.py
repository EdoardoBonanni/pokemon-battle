from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from models.Model import Model
from UI.StartGameUI import Ui_MainWindow
from battle_window import battle_window
from battle_window_multiplayer import battle_window_multiplayer
import random
from configuration_dialog import configuration_dialog
from copy import deepcopy

class start_battle_window(QMainWindow):
    def __init__(self, model: Model, choose_pokemon_view):
        super(start_battle_window, self).__init__()
        # get the Ui_MainWindow.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.parent_view = choose_pokemon_view
        self.model = model
        self.configuration_dialog = configuration_dialog()

        self.show()
        self.interaction()

    def interaction(self):
        self.ui.singleplayer.clicked.connect(self.start_singleplayer_battle)
        self.ui.multiplayer.clicked.connect(self.start_multiplayer_battle)
        self.ui.exit.clicked.connect(self.exit_action)

    def start_singleplayer_battle(self):
        if self.ui.insert_name.text() != '' and len(self.ui.insert_name.text()) < 25:
            self.model.me.name = self.ui.insert_name.text()
            self.choose_enemy_pokemon()

            # enemy
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Rattata']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Moltres']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Lickitung']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Machamp']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Fearow']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Dodrio']))

            battle_window_obj = battle_window(self.model, self.width(), self.height())
            self.hide()
            battle_window_obj.game()
            self.show()
            del battle_window_obj
        elif len(self.ui.insert_name.text()) >= 25:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle('Warning')
            msg_box.setWindowIcon(QtGui.QIcon('img/exclamation.png'))
            msg_box.setText("Nickname too long.")
            msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle('Warning')
            msg_box.setWindowIcon(QtGui.QIcon('img/exclamation.png'))
            msg_box.setText("You have to choose a nickname.")
            msg_box.exec_()

    def start_multiplayer_battle(self):
        if self.ui.insert_name.text() != '' and len(self.ui.insert_name.text()) < 25:
            self.model.me.name = self.ui.insert_name.text()

            battle_window_multiplayer_obj = battle_window_multiplayer(self.model, self.width(), self.height())
            self.hide()
            battle_window_multiplayer_obj.game()
            self.show()
            del battle_window_multiplayer_obj

            # data = {
            #     "type": "team",
            #     "pokemon_0": str(self.model.me.team[0].name.lower()),
            #     "pokemon_1": str(self.model.me.team[1].name.lower()),
            #     "pokemon_2": str(self.model.me.team[2].name.lower()),
            #     "pokemon_3": str(self.model.me.team[3].name.lower()),
            #     "pokemon_4": str(self.model.me.team[4].name.lower()),
            #     "pokemon_5": str(self.model.me.team[5].name.lower())
            # }

        elif len(self.ui.insert_name.text()) >= 25:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle('Warning')
            msg_box.setWindowIcon(QtGui.QIcon('img/exclamation.png'))
            msg_box.setText("Nickname too long.")
            msg_box.exec_()
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle('Warning')
            msg_box.setWindowIcon(QtGui.QIcon('img/exclamation.png'))
            msg_box.setText("You have to choose a nickname.")
            msg_box.exec_()

    def exit_action(self):
        self.model.me.team = []
        self.model.enemy.team = []
        self.hide()
        self.parent_view.update_team()
        self.parent_view.show()

    def choose_enemy_pokemon(self):
        while len(self.model.enemy.team) < 6:
            index = random.randint(0, len(self.model.pokedex.listPokemon) - 1)
            pokemon = deepcopy(list(self.model.pokedex.listPokemon.values())[index])
            if pokemon.name not in self.model.enemy.pokemon_names():
                self.model.enemy.add_pokemon(pokemon)

