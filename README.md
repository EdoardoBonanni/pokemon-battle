# Pokemon Battle Simulator
Pokémon Battle Simulator is a game that aims to simulate the real Pokémon battle games with an implementation based on PyGame. 
In the application are implemented all features and functionalities that allow the player to choose his team and play a match in **singleplayer** or **multiplayer** mode.

In the [**report**](https://github.com/EdoardoBonanni/pokemon-battle/blob/main/Pok%C3%A9mon%20Battle%20Simulator%20report.pdf), we will illustrate the entire **development process** of the application itself, starting from the motivations, passing through the implementation, models, wireframes and mockups, up to show the complete game and the several usability tests.

## Prerequisites
Package | Version
------- | -------
[Python](https://www.python.org) | 3.8
[PyQt](https://www.riverbankcomputing.com/software/pyqt/download5) | 5.9.2
[PyGame](https://www.pygame.org/docs) | 2.1.2
[PyGame Gui](https://pygame-gui.readthedocs.io/en/latest) | 0.6.1
[NumPy](https://numpy.org) | 1.22.1

The other modules requested are already available if you use Python 3.8.

## Usage
If you want to play singleplayer mode just launch **main.py** with python (if you have a virtual environment, remember to activate it) and select the singleplayer modality.
```
python main.py
```
Instead, if you choose the multiplayer mode, you need to run the server (**Server.py**).
```
python connection/Server.py
```
After that, two instances of the game must be run two times by launching **main.py**.
## GUI
The application is divided into vary main screens.
* **PokemonChoice** that is the first main screen of the application and allows the user to select all Pokémon for the team. 
For all Pokémon are shown their stats and their moves, so you can choose Pokémon based on their types and moves to develop a strategy against the other trainers. The add, remove buttons allow to do related operations in the Pokémon team and by clicking on a Pokémon of the team it's possible to switch directly with the one selected in the list. <br/>
![init_img.PNG](https://github.com/EdoardoBonanni/pokemon-battle/blob/main/img/init_img.PNG)

* **GameModeSelection** that allows to select the game mode or return to ChoosePokemon window. Before start a battle is mandatory to insert a nickname (be careful about the words you choose). <br/>
![select_mode.PNG](https://github.com/EdoardoBonanni/pokemon-battle/blob/main/img/select_mode.PNG)

* **BattleWindowSingleplayer** is the window that allows to play the game vs CPU in singleplayer mode. It's displayed the battlefield with the active Pokémon, their types, hp bars and moves. You can choose the Pokémon move for the turn, change active Pokémon or quit the game. <br/>
![singleplayer.PNG](https://github.com/EdoardoBonanni/pokemon-battle/blob/main/img/singleplayer.PNG)

* **BattleWindowMultiplayer** is the window that allows to play the game vs an other trainer in multiplayer mode. It's displayed the battlefield with the active Pokémon, their types, hp bars and moves. You can choose the Pokémon move for the turn, change active Pokémon or quit the game. <br/>
![multiplayer.PNG](https://github.com/EdoardoBonanni/pokemon-battle/blob/main/img/multiplayer.PNG)

* **TeamChoiceMenu** that allows to change the active Pokémon with an other in the team. This window is opened when you click 'Change Pokémon' button on BattleWindowSingleplayer/Multiplayer or when your active Pokémon is fainted. <br/>
![pokemon_team.PNG](https://github.com/EdoardoBonanni/pokemon-battle/blob/main/img/pokemon_team.PNG)
