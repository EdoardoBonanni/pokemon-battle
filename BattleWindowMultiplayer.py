from models.Model import Model
import pygame
import pygame_gui
from utility import utils, game_multiplayer, show_screen_elements
from connection.Network import Network
from copy import deepcopy
import ast, os, random


class BattleWindowMultiplayer:
    def __init__(self, model: Model, pos_x, pos_y):
        self.model = model
        self.names = None
        self.i = 0
        self.screen_width = 1300
        self.screen_height = int(1300 * 0.7)
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)

        self.init()

    def init(self):
        """
        Init of PyGame window.
        :return:
        """
        pygame.init()

        pygame.display.set_caption('Pokémon Battle Simulator')
        icon = pygame.image.load('img/logo.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # PyGame screen display.
        pygame.mixer.init()
        pygame.mixer.Channel(0).set_volume(0.05)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/battle_soundtrack.mp3'), -1)
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height),
                                            'themes/button_theming_test_theme.json')  # PyGame gui manager.
        self.font_name = pygame.font.Font("fonts/VT323-Regular.ttf", 60)
        self.font_hp = pygame.font.Font("fonts/VT323-Regular.ttf", 40)
        self.color_mapping = utils.create_color_mapping()
        self.description_battle = ''
        self.bg_color = (224, 235, 235)  # background color.

        # set framerate.
        self.clock = pygame.time.Clock()
        self.start_game = False

        self.names = list(self.model.pokedex.listPokemon.keys())
        self.move_up_back = []
        self.move_down_back = []
        self.move_up = []
        self.move_down = []

        self.net = Network()
        p = self.net.get_player()
        if p:
            self.player = int(p)
        else:
            self.player = None
        self.btn_quit = None

    def draw_bg(self):
        """
        Draw background and every fundamental component on the screen.
        :return:
        """
        if not self.draw_bg_img:
            self.battle_bg_img = pygame.image.load('img/battle_bg_1.png').convert_alpha()
            self.battle_bg_img = pygame.transform.scale(self.battle_bg_img,
                                                        (self.screen_width, self.screen_height * 0.79))
            self.hp_img_me = pygame.image.load('img/life_bar_player.png').convert_alpha()
            self.hp_img_me = pygame.transform.scale(self.hp_img_me, (
                self.hp_img_me.get_width() / 1.25, self.hp_img_me.get_height() / 1.25))
            self.hp_img_enemy = pygame.image.load('img/life_bar_enemy.png').convert_alpha()
            self.hp_img_enemy = pygame.transform.scale(self.hp_img_enemy, (
                self.hp_img_enemy.get_width() / 1.25, self.hp_img_enemy.get_height() / 1.25))
            self.name_player = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render("You: " + str(self.model.me.name),
                                                                                      False, (0, 0, 0))
            self.draw_bg_img = True
        self.screen.blit(self.battle_bg_img, (0, 0))
        # check if enemy is found.
        if self.name_enemy_found:
            self.screen.blit(self.hp_img_me, (self.screen_width * 0.63, self.screen_height * 0.55))
            self.screen.blit(self.hp_img_enemy, (self.screen_width * 0.08, self.screen_height * 0.15))
        self.screen.blit(self.name_player, (self.screen_width * 0.64, self.screen_height * 0.72))
        if self.name_enemy_found:
            self.name_enemy = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render(
                "Enemy: " + str(self.model.enemy.name), False, (0, 0, 0))
            self.screen.blit(self.name_enemy, (self.screen_width * 0.112, self.screen_height * 0.03))

    def draw_button(self, draw_button_change_pokemon):
        """
        Draw 'Change Pokemon' and 'Quit' buttons on the screen.
        :param draw_button_change_pokemon: Check if draw Change Pokemon button.
        :return:
        """
        button_width = self.screen_width * 0.18
        button_height = self.screen_height * 0.08
        if draw_button_change_pokemon:
            self.btn_change_pokemon = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen_width * 0.05, self.screen_height * 0.90),
                                          (button_width, button_height)),
                text='Change Pokemon',
                manager=self.manager,
                object_id='#btn_change_pokemon')
        if self.btn_quit is None:
            self.btn_quit = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen_width * 0.25, self.screen_height * 0.90),
                                          (button_width, button_height)),
                text='Quit',
                manager=self.manager,
                object_id='#btn_quit')

    def draw_fundamental_parts(self, draw_btn_change_pokemon):
        """
        Draw some objects on screen when player waiting for an opponent.
        :param draw_btn_change_pokemon: Check if draw Change Pokemon button.
        :return:
        """
        self.screen.fill(self.bg_color)
        self.draw_bg()
        show_screen_elements.draw_battle_description(self, self.description_battle)
        self.draw_button(draw_btn_change_pokemon)

    def update_battle_window(self, show_button, show_type_img):
        """
        Update battle window to show/hide objects on screen.
        :param show_button: choose if show/hide buttons.
        :param show_type_img: choose if show Pokemon move type images.
        :return:
        """
        self.screen.fill(self.bg_color)
        self.draw_bg()
        if self.start_battle:
            self.description_battle = str(self.model.me.team[0].name) + ' it\'s your turn.'
        show_screen_elements.draw_battle_description(self, self.description_battle)
        if not self.draw_button_battle:
            self.draw_button(True)
            show_screen_elements.draw_button_moves(self)
            self.draw_button_battle = True
        if show_button:
            self.btn_change_pokemon.show()
            self.btn_quit.show()
            self.btn_move1.show()
            self.btn_move2.show()
            self.btn_move3.show()
            self.btn_move4.show()
        else:
            show_screen_elements.hide_buttons(self)
        show_screen_elements.draw_pokemon(self, self.model.me.team[0], self.model.enemy.team[0], show_type_img)

    def reset_buttons(self):
        """
        Reset buttons values except for Quit button.
        :return:
        """
        if self.btn_change_pokemon:
            self.btn_change_pokemon.hide()
        if self.btn_move1:
            self.btn_move1.hide()
        if self.btn_move2:
            self.btn_move2.hide()
        if self.btn_move3:
            self.btn_move3.hide()
        if self.btn_move4:
            self.btn_move4.hide()
        self.btn_change_pokemon = None
        self.btn_move1 = None
        self.btn_move2 = None
        self.btn_move3 = None
        self.btn_move4 = None

    def keep_connection(self):
        """
        Keep connection with server.
        :return: a message received from server.
        """
        try:
            message = self.net.send_receive("get")
            self.enemy_lost_connection = False
        except:
            self.enemy_lost_connection = True
            print("game not ready")
            message = None
        return message

    def select_pokemon_from_menu_multiplayer(self, event, rect_menu, pokemon_index, pokemon_active, pokemon_changed,
                                             pokemon_withdrawn, new_pokemon_active):
        """
        Select a Pokemon from team in the choice menu.
        :param event: PyGame event.
        :param rect_menu: PyGame rect.
        :param pokemon_index: Pokemon index in the team.
        :param pokemon_active: Pokemon active in battle.
        :param pokemon_changed: check if Pokemon is changed or not.
        :param pokemon_withdrawn: Pokemon withdrawn from battle if player change it.
        :param new_pokemon_active: new Pokemon selected for the game.
        :return: pokemon_changed, pokemon_withdrawn, new_pokemon_active
        """
        if rect_menu.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if self.model.me.team[pokemon_index].battleHP_actual > 0:
                    if pokemon_active.battleHP_actual != 0:
                        self.pokemon_changed_not_fainted = True
                    utils.reset_stats(pokemon_active)
                    pokemon_withdrawn = pokemon_active
                    new_pokemon_active = self.model.me.team[pokemon_index]
                    self.special_moves_me = None
                    self.count_move_me = 0
                    self.model.me.swap_position(0, pokemon_index)
                    self.change_pokemon_menu = False
                    pokemon_changed = True
        return pokemon_changed, pokemon_withdrawn, new_pokemon_active

    def change_pokemon(self):
        """
        Change Pokemon on screen and show the other one that is chosen.
        :return: [pokemon_changed, pokemon_withdrawn, new_pokemon_active] = Returns if Pokemon is changed and if so return
        the Pokemon withdrawn and the new one, else None.
        """
        self.screen.fill(self.bg_color)
        show_screen_elements.hide_buttons(self)
        show_screen_elements.draw_team_choice_menu(self)
        show_screen_elements.draw_HP_pokemon_choice_menu(self)

        pokemon_changed = False
        pokemon_withdrawn = None
        new_pokemon_active = None

        for event in pygame.event.get():
            if self.rect_pokemon_list_menu_active.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[0].battleHP_actual > 0:
                        self.change_pokemon_menu = False
            pokemon_changed, pokemon_withdrawn, new_pokemon_active = self.select_pokemon_from_menu_multiplayer(event,
                                                                                                               self.rect_pokemon_list_menu_deactive1,
                                                                                                               1,
                                                                                                               self.model.me.team[
                                                                                                                   0],
                                                                                                               pokemon_changed,
                                                                                                               pokemon_withdrawn,
                                                                                                               new_pokemon_active)
            pokemon_changed, pokemon_withdrawn, new_pokemon_active = self.select_pokemon_from_menu_multiplayer(event,
                                                                                                               self.rect_pokemon_list_menu_deactive2,
                                                                                                               2,
                                                                                                               self.model.me.team[
                                                                                                                   0],
                                                                                                               pokemon_changed,
                                                                                                               pokemon_withdrawn,
                                                                                                               new_pokemon_active)
            pokemon_changed, pokemon_withdrawn, new_pokemon_active = self.select_pokemon_from_menu_multiplayer(event,
                                                                                                               self.rect_pokemon_list_menu_deactive3,
                                                                                                               3,
                                                                                                               self.model.me.team[
                                                                                                                   0],
                                                                                                               pokemon_changed,
                                                                                                               pokemon_withdrawn,
                                                                                                               new_pokemon_active)
            pokemon_changed, pokemon_withdrawn, new_pokemon_active = self.select_pokemon_from_menu_multiplayer(event,
                                                                                                               self.rect_pokemon_list_menu_deactive4,
                                                                                                               4,
                                                                                                               self.model.me.team[
                                                                                                                   0],
                                                                                                               pokemon_changed,
                                                                                                               pokemon_withdrawn,
                                                                                                               new_pokemon_active)
            pokemon_changed, pokemon_withdrawn, new_pokemon_active = self.select_pokemon_from_menu_multiplayer(event,
                                                                                                               self.rect_pokemon_list_menu_deactive5,
                                                                                                               5,
                                                                                                               self.model.me.team[
                                                                                                                   0],
                                                                                                               pokemon_changed,
                                                                                                               pokemon_withdrawn,
                                                                                                               new_pokemon_active)
            if self.rect_text_exit.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[0].battleHP_actual > 0:
                        self.change_pokemon_menu = False
        self.description_battle = 'What will ' + self.model.me.team[0].name + ' do?'
        return pokemon_changed, pokemon_withdrawn, new_pokemon_active

    def find_enemy_name(self):
        """
        Find the name of enemy that is connected in game.
        :return:
        """
        name_send = False
        k = 0
        wait = 5
        while k < wait:
            self.clock.tick(self.FPS)

            message = self.keep_connection()
            show_screen_elements.basic_events(self)
            if self.enemy_lost_connection:
                self.exit_battle = True
            if self.exit_battle:
                show_screen_elements.exit_battle_operations(self)
                self.description_battle = 'Connection lost with enemy, return to game mode selection.'
                self.connection_lost_waiting(100)
                break

            if message:
                if not message.data[self.player] and not name_send:
                    # players send their names.
                    data = {'type': 'send_player_name',
                            'player_name': str(self.model.me.name)
                            }
                    data_str = str(data)
                    self.net.send_receive(data_str)
                    name_send = True

                if message.both_went() and not self.name_enemy_found:
                    # players receive their names and add it to enemy model.
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data['type'] == 'send_player_name':
                        self.model.enemy.name = str(data['player_name'])
                        self.name_enemy_found = True
                        self.net.send_receive('reset')

                if not self.name_enemy_found:
                    self.description_battle = 'Waiting for a player ... '
                else:
                    self.description_battle = 'Connecting ... '
                    k = k + 1
            else:
                self.description_battle = 'Waiting for a player ... '
            self.draw_fundamental_parts(False)

            show_screen_elements.update_manager_and_display(self)

    def find_enemy_team(self):
        """
        Find enemy Pokemon team of the player that is connected in game.
        :return:
        """
        team_send = False
        k = 0
        wait = 5
        while k < wait:
            self.clock.tick(self.FPS)

            message = self.keep_connection()
            show_screen_elements.basic_events(self)
            if self.enemy_lost_connection:
                self.exit_battle = True
            if self.exit_battle:
                show_screen_elements.exit_battle_operations(self)
                self.description_battle = 'Connection lost with enemy, return to game mode selection.'
                self.connection_lost_waiting(100)
                break

            if message:
                if not message.data[self.player] and not team_send:
                    # players send their Pokemon team.
                    data = {'type': 'send_team',
                            'pokemon0': str(self.model.me.team[0].name),
                            'pokemon1': str(self.model.me.team[1].name),
                            'pokemon2': str(self.model.me.team[2].name),
                            'pokemon3': str(self.model.me.team[3].name),
                            'pokemon4': str(self.model.me.team[4].name),
                            'pokemon5': str(self.model.me.team[5].name)
                            }
                    data_str = str(data)
                    self.net.send_receive(data_str)
                    team_send = True

                if message.both_went() and not self.team_enemy_found:
                    # players receive their Pokemon team and add it to enemy model.
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data['type'] == 'send_team':
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon0'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon1'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon2'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon3'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon4'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon5'])]))
                        self.team_enemy_found = True
                        self.net.send_receive('reset')

                if self.name_enemy_found:
                    k = k + 1

            self.description_battle = 'Configuration phase ...'
            self.draw_fundamental_parts(False)

            show_screen_elements.update_manager_and_display(self)

    def find_enemy_move(self, attack, move, prob_accuracy, critic_value, pokemon_withdrawn, new_pokemon_active):
        """
        Find enemy move of the player that is connected in game.
        :param attack: Check if players attack or change their Pokemon.
        :param move: move Pokemon to send.
        :param prob_accuracy: prob_accuracy Pokemon to send.
        :param critic_value: critic_value Pokemon to send.
        :param pokemon_withdrawn: Pokemon withdrawn from battle or None to send.
        :param new_pokemon_active: new Pokemon in battle or None to send.
        :return:
        """
        move_send = False
        k = 0
        wait = 5
        while k < wait:
            self.clock.tick(self.FPS)

            message = self.keep_connection()
            show_screen_elements.basic_events(self)
            if self.enemy_lost_connection:
                self.exit_battle = True
            if self.exit_battle:
                show_screen_elements.exit_battle_operations(self)
                self.description_battle = 'Connection lost with enemy, return to game mode selection.'
                self.connection_lost_waiting(100)
                break

            if message:
                if not message.data[self.player] and not move_send:
                    # players send the moves.
                    if attack:
                        if self.special_moves_me:
                            special_move = str(self.special_moves_me.name)
                        else:
                            special_move = 'None'
                        self.prob_accuracy[0] = prob_accuracy
                        self.critic_value[0] = critic_value
                        data = {'type': 'attack',
                                'pokemon_active': str(self.model.me.team[0].name),
                                'move_pokemon': str(move.name),
                                'special_move': special_move,
                                'count_move': str(self.count_move_me),
                                'prob_accuracy': str(prob_accuracy),
                                'critic_value': str(critic_value)
                                }
                    else:
                        data = {'type': 'change_pokemon',
                                'pokemon_withdrawn': str(pokemon_withdrawn.name),
                                'new_pokemon_active': str(new_pokemon_active.name)
                                }
                    data_str = str(data)
                    self.net.send_receive(data_str)
                    move_send = True

                if message.both_went() and not self.move_enemy_found:
                    # players receive the enemy move.
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data['type'] == 'attack':
                        self.enemy_move_data = deepcopy(data)
                        self.enemy_use_attack = True
                        self.move_enemy_found = True
                        self.net.send_receive('reset')
                    elif data['type'] == 'change_pokemon':
                        self.enemy_move_data = deepcopy(data)
                        self.move_enemy_found = True
                        self.net.send_receive('reset')

                if self.move_enemy_found:
                    k = k + 1

            self.description_battle = 'Waiting for enemy move ...'
            self.update_battle_window(False, False)
            show_screen_elements.draw_hp(self, self.model.me.team[0].battleHP_actual,
                                         self.model.enemy.team[0].battleHP_actual)

            show_screen_elements.update_manager_and_display(self)

    def find_pokemon_fainted(self):
        """
        Find if a Pokemon is fainted of the player that is connected in game.
        :return:
        """
        pokemon_fainted_send = False
        k = 0
        wait = 5
        while k < wait:
            self.clock.tick(self.FPS)

            message = self.keep_connection()
            show_screen_elements.basic_events(self)
            if self.enemy_lost_connection:
                self.exit_battle = True
            if self.exit_battle:
                show_screen_elements.exit_battle_operations(self)
                self.description_battle = 'Connection lost with enemy, return to game mode selection.'
                self.connection_lost_waiting(100)
                break

            if message:
                if not message.data[self.player] and not pokemon_fainted_send:
                    # players send Pokemon withdrawn and the new one in battle if Pokemon fainted, else None.
                    if self.pokemon_withdrawn and self.new_pokemon_active:
                        data = {'type': 'change_pokemon_fainted',
                                'pokemon_withdrawn': str(self.pokemon_withdrawn.name),
                                'new_pokemon_active': str(self.new_pokemon_active.name)
                                }
                    else:
                        data = {'type': 'change_pokemon_fainted',
                                'pokemon_withdrawn': 'None',
                                'new_pokemon_active': 'None'
                                }
                    data_str = str(data)
                    self.net.send_receive(data_str)
                    pokemon_fainted_send = True

                if message.both_went() and not self.pokemon_fainted_found:
                    # players receive Pokemon withdrawn and the new one in battle if Pokemon fainted, else None.
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data['type'] == 'change_pokemon_fainted':
                        self.pokemon_fainted_found = True
                        self.net.send_receive('reset')
                        if str(data['pokemon_withdrawn']) != 'None' and str(data['new_pokemon_active']) != 'None':
                            self.switch_enemy_pokemon(str(data['new_pokemon_active']))

                if self.pokemon_fainted_found:
                    k = k + 1

            self.description_battle = 'Waiting for enemy selection ...'
            self.update_battle_window(False, False)
            show_screen_elements.draw_hp(self, self.model.me.team[0].battleHP_actual,
                                         self.model.enemy.team[0].battleHP_actual)

            show_screen_elements.update_manager_and_display(self)

    def connection_lost_waiting(self, wait):
        """
        Remain in game and waiting a new player if connection is lost with the enemy.
        :param wait: time to wait.
        :return:
        """
        k = 0
        while k < wait:
            self.clock.tick(self.FPS)
            show_screen_elements.basic_events(self)

            self.draw_fundamental_parts(False)

            show_screen_elements.update_manager_and_display(self)
            k += 1

    def show_error_server_off(self, wait):
        """
        Show the error message due to server off.
        :param wait: time to wait.
        :return:
        """
        k = 0
        while k < wait:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                self.manager.process_events(event)

            self.screen.fill(self.bg_color)
            message_server_off = pygame.font.Font("fonts/VT323-Regular.ttf", 60).render(
                'Start the server for multiplayer mode', False, (0, 0, 0))
            self.screen.blit(message_server_off, (self.screen_width * 0.17, self.screen_height * 0.45))

            show_screen_elements.update_manager_and_display(self)
            k += 1

    def read_data_moves(self):
        """
        Read data from packets received and check player move type to update enemy model.
        :return:
        """
        if self.enemy_use_attack:
            if self.enemy_move_data['type'] == 'attack':
                move_pokemon_str = str(self.enemy_move_data['move_pokemon'])
                self.move_enemy = utils.search_move_pokemon(self.model.enemy.team[0], move_pokemon_str)
                special_move_str = str(self.enemy_move_data['special_move'])
                if special_move_str != 'None':
                    self.special_moves_enemy = utils.search_move_pokemon(self.model.enemy.team[0], special_move_str)
                else:
                    self.special_moves_enemy = None
                self.count_move_enemy = int(self.enemy_move_data['count_move'])
                self.prob_accuracy[1] = float(self.enemy_move_data['prob_accuracy'])
                self.critic_value[1] = float(self.enemy_move_data['critic_value'])
        else:
            if self.enemy_move_data['type'] == 'change_pokemon':
                # todo check if exist.
                pokemon_withdrawn_str = str(self.enemy_move_data['pokemon_withdrawn'])
                new_pokemon_active_str = str(self.enemy_move_data['new_pokemon_active'])
                self.switch_enemy_pokemon(new_pokemon_active_str)

    def switch_enemy_pokemon(self, new_pokemon_active_name):
        """
        Switch the enemy Pokemon and show the animations related.
        :param new_pokemon_active_name: Name of the new enemy Pokemon in game.
        :return:
        """
        index = utils.search_pokemon(self.model.enemy.team, new_pokemon_active_name)
        utils.reset_stats(self.model.enemy.team[0])
        self.model.enemy.swap_position(0, index)
        self.pokemon_enemy_visible = False
        show_screen_elements.pokeball_animations(self, 10, False, False, False, self.model.me.team[0],
                                                 self.model.enemy.team[0], False, True)
        show_screen_elements.pokeball_animations(self, 10, False, False, True, self.model.me.team[0],
                                                 self.model.enemy.team[0], False, True)
        self.pokemon_enemy_visible = True

    def read_players_attack(self, move_me):
        """
        Read players attack and start the game turn.
        :param move_me: move player me.
        :return:
        """
        prob_accuracy = random.random() * 100
        critic_value = random.uniform(0.80, 1.0)
        self.find_enemy_move(True, move_me, prob_accuracy, critic_value, None, None)
        if self.move_enemy_found and self.enemy_move_data:
            self.read_data_moves()
            game_multiplayer.checks_2_turns_attack(self, move_me, self.move_enemy, self.prob_accuracy,
                                                   self.critic_value)

    def battle_events_multiplayer(self, event, button_move, move_id):
        """
        Check the move choice and after that all animation start.
        :param event: PyGame event.
        :param button_move: one of the four button move.
        :param move_id: one of the four Pokemon move.
        :return:
        """
        if event.ui_element.most_specific_combined_id == button_move.most_specific_combined_id:
            if move_id.pp_remain > 0:
                self.read_players_attack(move_id)
            else:
                self.description_battle = move_id.name + ' has 0 pp left.'
                show_screen_elements.wait(self, 30, False, False)

    def game(self):
        """
        Game function that uses all functions to run the script and handle events.
        :return:
        """
        self.FPS = 40
        self.run = True

        self.start_battle = True
        self.draw_bg_img = False
        self.draw_button_battle = False
        self.change_pokemon_menu = False
        self.pokemon_changed_not_fainted = False
        self.count_move_me = 0
        self.count_move_enemy = 0
        self.special_moves_me = None
        self.special_moves_enemy = None
        self.pokemon_me_visible = False
        self.pokemon_enemy_visible = False

        # check if server is on.
        if self.player == 0 or self.player == 1:
            self.server_off = False
        else:
            self.server_off = True
        self.exit_battle = False
        self.pokemon_fainted = False
        self.pokemon_me_fainted = False
        self.pokemon_enemy_fainted = False

        self.explosion_sheet = utils.read_spritesheet_explosion('img/explosion_sheet.png')
        trainer_me = utils.read_spritesheet_trainer_me('img/trainer_sheet.png')
        trainer_enemy = utils.read_spritesheet_trainer_enemy('img/enemy_trainers_sheet.png')
        start_animations = True

        self.pokemon_withdrawn = None
        self.new_pokemon_active = None
        self.move_enemy = None
        self.prob_accuracy = [None, None]
        self.critic_value = [None, None]

        self.enemy_lost_connection = False
        self.name_enemy_found = False
        self.team_enemy_found = False
        self.move_enemy_found = False
        self.enemy_use_attack = False
        self.enemy_move_data = None
        self.pokemon_fainted_found = False

        # while to run the Game.
        while self.run:
            self.clock.tick(self.FPS)
            _ = self.keep_connection()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_battle = True
                    self.run = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.btn_change_pokemon:
                        if event.ui_element.most_specific_combined_id == self.btn_change_pokemon.most_specific_combined_id:
                            self.change_pokemon_menu = True
                    if event.ui_element.most_specific_combined_id == self.btn_quit.most_specific_combined_id:
                        self.exit_battle = True
                    self.battle_events_multiplayer(event, self.btn_move1, self.model.me.team[0].move1)
                    self.battle_events_multiplayer(event, self.btn_move2, self.model.me.team[0].move2)
                    self.battle_events_multiplayer(event, self.btn_move3, self.model.me.team[0].move3)
                    self.battle_events_multiplayer(event, self.btn_move4, self.model.me.team[0].move4)

                self.manager.process_events(event)

            # check if server is off.
            if self.server_off:
                self.show_error_server_off(50)
                pygame.quit()
                return None
            else:
                # exit from Game and return to GameModeSelection.
                if self.exit_battle:
                    show_screen_elements.exit_battle_operations(self)
                    pygame.quit()
                    return None
                # check if enemy lost connection.
                if not self.enemy_lost_connection:
                    # check if enemy name is found.
                    if not self.name_enemy_found:
                        self.find_enemy_name()
                    else:
                        # check if enemy team is found.
                        if not self.team_enemy_found:
                            self.find_enemy_team()
                        else:
                            self.move_enemy_found = False
                            self.enemy_use_attack = False
                            self.enemy_move_data = None
                            self.move_enemy = None
                            self.prob_accuracy = [None, None]
                            self.critic_value = [None, None]
                            # check if players Pokemon in battle are fainted.
                            if self.pokemon_fainted:
                                # check if player me Pokemon is fainted, else enemy.
                                if self.pokemon_me_fainted:
                                    change_pokemon, self.pokemon_withdrawn, self.new_pokemon_active = self.change_pokemon()
                                    # check if Pokemon is changed.
                                    if change_pokemon:
                                        self.pokemon_me_visible = False
                                        show_screen_elements.pokeball_animations(self, 10, False, False, False,
                                                                                 self.model.me.team[0],
                                                                                 self.model.enemy.team[0], True, False)
                                        show_screen_elements.pokeball_animations(self, 10, False, False, True,
                                                                                 self.model.me.team[0],
                                                                                 self.model.enemy.team[0], True, False)
                                        self.pokemon_me_visible = True
                                        # check if enemy Pokemon fainted is found.
                                        if not self.pokemon_fainted_found:
                                            self.find_pokemon_fainted()
                                            if self.pokemon_fainted_found:
                                                self.pokemon_fainted = False
                                                self.pokemon_me_fainted = False
                                                self.pokemon_enemy_fainted = False
                                                self.pokemon_fainted_found = False
                                else:
                                    self.pokemon_withdrawn = None
                                    self.new_pokemon_active = None
                                    # check if enemy Pokemon fainted is found.
                                    if not self.pokemon_fainted_found:
                                        self.find_pokemon_fainted()
                                        if self.pokemon_fainted_found:
                                            self.pokemon_fainted = False
                                            self.pokemon_me_fainted = False
                                            self.pokemon_enemy_fainted = False
                                            self.pokemon_fainted_found = False
                            else:
                                self.pokemon_fainted = False
                                self.pokemon_me_fainted = False
                                self.pokemon_enemy_fainted = False
                                # check if Pokemon in battle is changed and not fainted, if so the enemy has to attack.
                                if self.pokemon_changed_not_fainted:
                                    self.find_enemy_move(False, None, None, None, self.pokemon_withdrawn,
                                                         self.new_pokemon_active)
                                    # check if enemy move and data are found.
                                    if self.move_enemy_found and self.enemy_move_data:
                                        self.read_data_moves()
                                        game_multiplayer.checks_2_turns_attack(self, None, self.move_enemy,
                                                                               self.prob_accuracy, self.critic_value)
                                # check if Pokemon of player me do a special move and calculate its values.
                                elif self.special_moves_me is not None:
                                    prob_accuracy = random.random() * 100
                                    critic_value = random.uniform(0.85, 1.0)
                                    self.find_enemy_move(True, self.special_moves_me, prob_accuracy, critic_value, None,
                                                         None)
                                    # check if enemy move and data are found.
                                    if self.move_enemy_found and self.enemy_move_data:
                                        self.read_data_moves()
                                        game_multiplayer.checks_2_turns_attack(self, self.special_moves_me,
                                                                               self.move_enemy, self.prob_accuracy,
                                                                               self.critic_value)
                                else:
                                    if not self.change_pokemon_menu:
                                        # check if the Game is started and if so run the first animations.
                                        if start_animations:
                                            show_screen_elements.start_battle_animations(self, trainer_me,
                                                                                         trainer_enemy, False, False)
                                            show_screen_elements.pokeball_animations(self, 10, False, False, False,
                                                                                     self.model.me.team[0],
                                                                                     self.model.enemy.team[0], True,
                                                                                     True)
                                            show_screen_elements.pokeball_animations(self, 10, False, False, True,
                                                                                     self.model.me.team[0],
                                                                                     self.model.enemy.team[0], True,
                                                                                     True)
                                            start_animations = False
                                            self.pokemon_me_visible = True
                                            self.pokemon_enemy_visible = True
                                        # normal execution of the Game.
                                        else:
                                            self.update_battle_window(True, True)
                                            show_screen_elements.draw_hp(self, self.model.me.team[0].battleHP_actual,
                                                                         self.model.enemy.team[0].battleHP_actual)
                                        self.start_battle = False
                                        self.description_battle = 'What will ' + self.model.me.team[0].name + ' do?'
                                    # check if the change Pokemon menu is active.
                                    else:
                                        change_pokemon, self.pokemon_withdrawn, self.new_pokemon_active = self.change_pokemon()
                                        # Check if user change Pokemon and if so the animation start.
                                        if change_pokemon:
                                            self.pokemon_me_visible = False
                                            show_screen_elements.pokeball_animations(self, 10, False, False, False,
                                                                                     self.model.me.team[0],
                                                                                     self.model.enemy.team[0], True,
                                                                                     False)
                                            show_screen_elements.pokeball_animations(self, 10, False, False, True,
                                                                                     self.model.me.team[0],
                                                                                     self.model.enemy.team[0], True,
                                                                                     False)
                                            self.pokemon_me_visible = True
                # reset all variables if connection with enemy is lost.
                else:
                    self.pokemon_me_visible = False
                    self.pokemon_enemy_visible = False
                    self.draw_button_battle = False
                    self.change_pokemon_menu = False
                    self.pokemon_changed_not_fainted = False
                    self.reset_buttons()
                    self.name_enemy_found = False
                    self.team_enemy_found = False
                    self.move_enemy_found = False
                    self.pokemon_fainted_found = False
                    self.pokemon_fainted_data = None
                    self.enemy_use_attack = False
                    self.enemy_move_data = None
                    self.pokemon_withdrawn = None
                    self.new_pokemon_active = None
                    self.move_enemy = None
                    self.prob_accuracy = [None, None]
                    self.critic_value = [None, None]
                    self.count_move_me = 0
                    self.count_move_enemy = 0
                    self.special_moves_me = None
                    self.special_moves_enemy = None
                    self.model.enemy.name = ''
                    self.model.enemy.team = []
                    utils.reset_team_stats(self.model.me)
                    self.start_battle = True
                    start_animations = True
                    self.description_battle = 'Connection lost with enemy.'
                    self.connection_lost_waiting(30)
                    self.net = Network()
                    self.player = int(self.net.get_player())

            show_screen_elements.update_manager_and_display(self)
        pygame.quit()
