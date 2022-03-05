from models.Model import Model
import pygame
from pygame.locals import *
import pygame_gui
from utility import utils
from connection.network import Network
from copy import deepcopy
import ast

#define colours
BG_GREEN = (144, 201, 120)
BG = (224, 235, 235)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

class battle_window_multiplayer:
    def __init__(self, model: Model, width, height):
        self.model = model
        self.names = None
        self.i = 0
        self.screen_width = 1300
        self.screen_height = int(1300 * 0.7)

        self.init()

    def init(self):
        pygame.init()

        pygame.display.set_caption('Pokemon Battle')
        icon = pygame.image.load('img/logo.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height), 'themes/button_theming_test_theme.json')
        self.font_name = pygame.font.Font("fonts/VT323-Regular.ttf", 60)
        self.font_hp = pygame.font.Font("fonts/VT323-Regular.ttf", 40)
        self.color_mapping = utils.create_color_mapping()
        self.description_battle = ''

        #set framerate
        self.clock = pygame.time.Clock()
        self.start_game = False

        self.names = list(self.model.pokedex.listPokemon.keys())
        self.move_up_back = []
        self.move_down_back = []
        self.move_up = []
        self.move_down = []

        self.net = Network()
        self.player = int(self.net.getP())

    def draw_bg(self):
        if not self.draw_bg_img:
            self.battle_bg_img = pygame.image.load('img/battle_bg_1.png').convert_alpha()
            self.battle_bg_img = pygame.transform.scale(self.battle_bg_img, (self.screen_width, self.screen_height * 0.79))
            self.hp_img_me = pygame.image.load('img/life_bar_player.png').convert_alpha()
            self.hp_img_me = pygame.transform.scale(self.hp_img_me, (self.hp_img_me.get_width() / 1.25, self.hp_img_me.get_height() / 1.25))
            self.hp_img_enemy = pygame.image.load('img/life_bar_enemy.png').convert_alpha()
            self.hp_img_enemy = pygame.transform.scale(self.hp_img_enemy, (self.hp_img_enemy.get_width() / 1.25, self.hp_img_enemy.get_height() / 1.25))
            self.name_player = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render("You: " + str(self.model.me.name), False, (0,0,0))
            self.draw_bg_img = True
        self.screen.blit(self.battle_bg_img, (0, 0))
        if self.name_enemy_found:
            self.screen.blit(self.hp_img_me, (self.screen_width * 0.63, self.screen_height * 0.55))
            self.screen.blit(self.hp_img_enemy, (self.screen_width * 0.08, self.screen_height * 0.15))
        self.screen.blit(self.name_player, (self.screen_width * 0.64, self.screen_height * 0.72))
        if self.name_enemy_found:
            self.name_enemy = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render("Enemy: " + str(self.model.enemy.name), False, (0,0,0))
            self.screen.blit(self.name_enemy, (self.screen_width * 0.112, self.screen_height * 0.03))

    def draw_battle_description(self, text):
        self.battle_description = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render(text, False, (0,0,0))
        self.screen.blit(self.battle_description, (self.screen_width * 0.04, self.screen_height * 0.825))

    def draw_button(self, draw_button_change_pokemon):
        button_width = self.screen_width * 0.18
        button_height = self.screen_height * 0.08
        if draw_button_change_pokemon:
            self.btn_change_pokemon = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.05, self.screen_height * 0.90),
                                                                                             (button_width, button_height)),
                                                                   text='Change Pokemon',
                                                                   manager=self.manager,
                                                                   object_id='#btn_change_pokemon')

        self.btn_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.25, self.screen_height * 0.90),
                                                                               (button_width, button_height)),
                                                     text='Quit',
                                                     manager=self.manager,
                                                     object_id='#btn_quit')

    def draw_fondamental_parts(self, draw_btn_change_pokemon):
        self.screen.fill(BG)
        self.draw_bg()
        self.draw_battle_description(self.description_battle)
        self.draw_button(draw_btn_change_pokemon)

    def keep_connection(self):
        try:
            message = self.net.send("get")
            self.enemy_lost_connection = False
        except:
            self.enemy_lost_connection = True
            print("game not ready")
            message = None
        return message

    def exit_battle_operations(self):
        utils.reset_team_stats(self.model.me)
        utils.reset_team_stats(self.model.enemy)
        self.model.enemy.team = []
        self.model.enemy.name = ''
        self.run = False

    def basic_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element.most_specific_combined_id == self.btn_quit.most_specific_combined_id:
                    self.exit_battle = True
            self.manager.process_events(event)

    def update_manager_and_display(self):
        time_delta = self.clock.tick(self.FPS)/1000.0
        self.manager.update(time_delta)

        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def find_enemy_name(self):
        name_send = False
        k = 0
        wait = 5
        while k < wait:
            self.clock.tick(self.FPS)

            message = self.keep_connection()
            self.basic_events()

            if self.exit_battle:
                self.exit_battle_operations()
                break

            if message:
                if not message.data[self.player] and not name_send:
                    self.net.send(self.model.me.name)
                    name_send = True

                if message.both_went() and not self.name_enemy_found:
                    other_player = (self.player + 1) % 2
                    self.model.enemy.name = str(message.get_data(other_player))
                    self.name_enemy_found = True
                    self.net.send('reset')

                if not self.name_enemy_found:
                    self.description_battle = 'Waiting for a player ... '
                else:
                    self.description_battle = 'Connecting ... '
                    k = k + 1
            else:
                self.description_battle = 'Waiting for a player ... '
            self.draw_fondamental_parts(False)

            self.update_manager_and_display()

    def find_enemy_team(self):
        team_send = False
        k = 0
        wait = 5
        while k < wait:
            self.clock.tick(self.FPS)

            message = self.keep_connection()
            self.basic_events()

            if self.exit_battle:
                self.exit_battle_operations()
                break

            if message:
                if not message.data[self.player] and not team_send:
                    data = {'type': 'send_team',
                            'pokemon0': str(self.model.me.team[0].name),
                            'pokemon1': str(self.model.me.team[1].name),
                            'pokemon2': str(self.model.me.team[2].name),
                            'pokemon3': str(self.model.me.team[3].name),
                            'pokemon4': str(self.model.me.team[4].name),
                            'pokemon5': str(self.model.me.team[5].name)
                    }
                    data_str = str(data)
                    self.net.send(data_str)
                    team_send = True

                if message.both_went() and not self.team_enemy_found:
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data.type == 'send_team':
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data.pokemon5)]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data.pokemon4)]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data.pokemon3)]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data.pokemon2)]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data.pokemon1)]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data.pokemon0)]))
                        self.team_enemy_found = True
                        self.net.send('reset')

                if self.name_enemy_found:
                    k = k + 1

            self.description_battle = 'Configuration phase ...'
            self.draw_fondamental_parts(False)

            self.update_manager_and_display()

    def game(self):
        self.FPS = 60
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
        self.exit_battle = False

        self.explosion_sheet = utils.read_spritesheet_explosion('img/explosion_sheet.png')
        trainer_me = utils.read_spritesheet_trainer_me('img/trainer_sheet.png')
        trainer_enemy = utils.read_spritesheet_trainer_enemy('img/enemy_trainers_sheet.png')
        start_animations = True

        #print('You are player: ', str(self.player))
        self.enemy_lost_connection = False
        self.name_enemy_found = False
        self.team_enemy_found = False

        while self.run:
            self.clock.tick(self.FPS)

            message = self.keep_connection()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element.most_specific_combined_id == self.btn_quit.most_specific_combined_id:
                        self.exit_battle = True

                self.manager.process_events(event)

            if self.exit_battle:
                self.exit_battle_operations()
                pygame.quit()
                return None

            if not self.enemy_lost_connection:
                if not self.name_enemy_found:
                    self.find_enemy_name()
                else:
                    if not self.team_enemy_found:
                        self.find_enemy_team()
                    else:
                        self.description_battle = 'ok'
                        self.draw_fondamental_parts(False)
            else:
                self.name_enemy_found = False
                self.model.enemy.name = ''
                self.net = Network()
                self.player = int(self.net.getP())

            self.update_manager_and_display()
        pygame.quit()









