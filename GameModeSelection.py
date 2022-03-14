from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from models.Model import Model
from UI.GameModeSelectionUI import Ui_MainWindow
from BattleWindowSingleplayer import BattleWindowSingleplayer
from BattleWindowMultiplayer import BattleWindowMultiplayer
import random
from copy import deepcopy


class GameModeSelection(QMainWindow):
    """
    GameModeSelection class used to select a game mode or return to the team selection.
    """
    def __init__(self, model: Model, choose_pokemon_view, pos_x, pos_y):
        super(GameModeSelection, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, pos_x, pos_y)

        self.parent_view = choose_pokemon_view
        self.model = model

        self.show()
        self.interaction()

    def interaction(self):
        """
        Function that allow to interact with every element of the window.
        :return:
        """
        self.ui.singleplayer.clicked.connect(self.start_singleplayer)
        self.ui.multiplayer.clicked.connect(self.start_multiplayer)
        self.ui.exit.clicked.connect(self.exit_action)

    def start_singleplayer(self):
        """
        Start the Single-Player mode if conditions are satisfied.
        :return:
        """
        if self.ui.insert_name.text() != '' and len(self.ui.insert_name.text()) < 25:
            self.model.me.name = self.ui.insert_name.text()
            self.choose_enemy_pokemon()

            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Dragonite']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Moltres']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Lickitung']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Machamp']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Fearow']))
            # self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon['Dodrio']))

            battle_window_singleplayer_obj = BattleWindowSingleplayer(self.model, self.pos().x() + 20, self.pos().y() + 25)
            self.hide()
            battle_window_singleplayer_obj.game()
            self.show()
            del battle_window_singleplayer_obj
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

    def start_multiplayer(self):
        """
        Start the Multi-Player mode if conditions are satisfied.
        :return:
        """
        if self.ui.insert_name.text() != '' and len(self.ui.insert_name.text()) < 25:
            self.model.me.name = self.ui.insert_name.text()

            battle_window_multiplayer_obj = BattleWindowMultiplayer(self.model, self.pos().x() + 20, self.pos().y() + 25)
            self.hide()
            battle_window_multiplayer_obj.game()
            self.show()
            del battle_window_multiplayer_obj

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
        """
        Return to the team selection and reset the teams.
        :return:
        """
        self.model.me.team = []
        self.model.enemy.team = []
        self.hide()
        self.parent_view.update_team()
        self.parent_view.show()

    def choose_enemy_pokemon(self):
        """
        Choose enemy team for Single-Player mode.
        :return:
        """
        while len(self.model.enemy.team) < 6:
            index = random.randint(0, len(self.model.pokedex.listPokemon) - 1)
            pokemon = deepcopy(list(self.model.pokedex.listPokemon.values())[index])
            if pokemon.name not in self.model.enemy.pokemon_names():
                self.model.enemy.add_pokemon(pokemon)