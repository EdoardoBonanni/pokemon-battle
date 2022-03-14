from models.Model import Model
import pygame
from pygame.locals import *
import pygame_gui
from utility import utils
from utility import game_multiplayer
from connection.Network import Network
from copy import deepcopy
import ast, os, random

# define colours.
BG_GREEN = (144, 201, 120)
BG = (224, 235, 235)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

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

        pygame.display.set_caption('Pokemon Battle')
        icon = pygame.image.load('img/logo.png')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # PyGame screen display.
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height), 'themes/button_theming_test_theme.json')  # PyGame gui manager.
        self.font_name = pygame.font.Font("fonts/VT323-Regular.ttf", 60)
        self.font_hp = pygame.font.Font("fonts/VT323-Regular.ttf", 40)
        self.color_mapping = utils.create_color_mapping()
        self.description_battle = ''

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
            self.battle_bg_img = pygame.transform.scale(self.battle_bg_img, (self.screen_width, self.screen_height * 0.79))
            self.hp_img_me = pygame.image.load('img/life_bar_player.png').convert_alpha()
            self.hp_img_me = pygame.transform.scale(self.hp_img_me, (self.hp_img_me.get_width() / 1.25, self.hp_img_me.get_height() / 1.25))
            self.hp_img_enemy = pygame.image.load('img/life_bar_enemy.png').convert_alpha()
            self.hp_img_enemy = pygame.transform.scale(self.hp_img_enemy, (self.hp_img_enemy.get_width() / 1.25, self.hp_img_enemy.get_height() / 1.25))
            self.name_player = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render("You: " + str(self.model.me.name), False, (0,0,0))
            self.draw_bg_img = True
        self.screen.blit(self.battle_bg_img, (0, 0))
        # check if enemy is found.
        if self.name_enemy_found:
            self.screen.blit(self.hp_img_me, (self.screen_width * 0.63, self.screen_height * 0.55))
            self.screen.blit(self.hp_img_enemy, (self.screen_width * 0.08, self.screen_height * 0.15))
        self.screen.blit(self.name_player, (self.screen_width * 0.64, self.screen_height * 0.72))
        if self.name_enemy_found:
            self.name_enemy = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render("Enemy: " + str(self.model.enemy.name), False, (0,0,0))
            self.screen.blit(self.name_enemy, (self.screen_width * 0.112, self.screen_height * 0.03))

    def draw_battle_description(self, text):
        """
        Draw text on the screen.
        :param text: battle description text.
        :return:
        """
        self.battle_description = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render(text, False, (0,0,0))
        self.screen.blit(self.battle_description, (self.screen_width * 0.04, self.screen_height * 0.825))

    def draw_button(self, draw_button_change_pokemon):
        """
        Draw 'Change Pokemon' and 'Quit' buttons on the screen.
        :param draw_button_change_pokemon: Check if draw Change Pokemon button.
        :return:
        """
        button_width = self.screen_width * 0.18
        button_height = self.screen_height * 0.08
        if draw_button_change_pokemon:
            self.btn_change_pokemon = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.05, self.screen_height * 0.90),
                                                                                             (button_width, button_height)),
                                                                   text='Change Pokemon',
                                                                   manager=self.manager,
                                                                   object_id='#btn_change_pokemon')
        if self.btn_quit is None:
            self.btn_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.25, self.screen_height * 0.90),
                                                                                   (button_width, button_height)),
                                                         text='Quit',
                                                         manager=self.manager,
                                                         object_id='#btn_quit')

    def draw_button_moves(self):
        """
        Draw Pokemon moves buttons on the screen.
        :return:
        """
        button_width = self.screen_width * 0.18
        button_height = self.screen_height * 0.08
        self.btn_move1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.58, self.screen_height * 0.81),
                                                                                (button_width, button_height)),
                                                      text='move1',
                                                      manager=self.manager,
                                                      object_id='#btn_move1')

        self.btn_move2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.78, self.screen_height * 0.81),
                                                                                (button_width, button_height)),
                                                      text='move2',
                                                      manager=self.manager,
                                                      object_id='#btn_move2')
        self.btn_move3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.58, self.screen_height * 0.90),
                                                                                (button_width, button_height)),
                                                      text='move3',
                                                      manager=self.manager,
                                                      object_id='#btn_move3')
        self.btn_move4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.78, self.screen_height * 0.90),
                                                                                (button_width, button_height)),
                                                      text='move4',
                                                      manager=self.manager,
                                                      object_id='#btn_move4')

    def draw_pokemon(self, pokemon_me, pokemon_enemy, show_type_img):
        """
        Draw Pokemon and all their attributes: name, moves, color buttons.
        :param pokemon_me: Pokemon me.
        :param pokemon_enemy: Pokemon enemy.
        :param show_type_img: choose if show Pokemon move type images.
        :return:
        """

        # Pokemon player me.
        # Move up/down several Pokemon on the screen for the correct position.
        if len(self.move_up_back) == 0:
            self.move_up_back = ['charizard', 'pidgeotto', 'fearow', 'arcanine', 'machamp', 'victreebel', 'dodrio', 'articuno', 'kangaskhan', 'gyarados', 'dragonite', 'rapidash', 'onix']
        if len(self.move_down_back) == 0:
            self.move_down_back = ['bulbasaur', 'ivysaur', 'charmander', 'squirtle', 'caterpie', 'metapod', 'kakuna', 'weedle', 'starly', 'pidgey', 'rattata', 'spearow', 'ekans', 'pikachu',
                                   'sandshrew', 'sandslash', 'nidoran', 'nidorina', 'clefairy', 'vulpix', 'jigglypuff', 'oddish', 'gloom', 'paras', 'venonat',
                                   'diglett', 'dugtrio', 'meowth', 'psyduck', 'mankey', 'growlithe', 'poliwag', 'poliwhirl', 'abra', 'bellsprout', 'geodude', 'graveler', 'slowpoke', 'magnemite',
                                   'seel', 'grimer', 'shellder', 'krabby', 'voltorb', 'exeggcute', 'cubone', 'marowak', 'chansey', 'tangela', 'horsea', 'seadra', 'goldeen', 'seaking',
                                   'staryu', 'ditto', 'jolteon', 'omanyte', 'porygon', 'kabuto']

        if self.pokemon_me_visible:
            pokemon_me_image = pygame.image.load('img_pokemon_battle_png/' + pokemon_me.name.lower() + '_back.png').convert_alpha()
            pokemon_me_image = pygame.transform.scale(pokemon_me_image, (pokemon_me_image.get_width() * 5, pokemon_me_image.get_height() * 5))
            if pokemon_me.name.lower() in self.move_up_back:
                self.screen.blit(pokemon_me_image, (self.screen_width * 0.04, self.screen_height * 0.28))
            elif pokemon_me.name.lower() in self.move_down_back:
                self.screen.blit(pokemon_me_image, (self.screen_width * 0.04, self.screen_height * 0.39))
            else:
                self.screen.blit(pokemon_me_image, (self.screen_width * 0.04, self.screen_height * 0.33))
        self.draw_types_pokemon_img(pokemon_me.type1, pokemon_me.type2, True)
        draw_name_me = self.font_name.render(pokemon_me.name, False, (0,0,0))
        self.screen.blit(draw_name_me, (self.screen_width * 0.67, self.screen_height * 0.475))
        self.btn_move1.set_text(str(pokemon_me.move1.name) + ' ' + str(pokemon_me.move1.pp_remain) + '/' + str(pokemon_me.move1.pp))
        self.btn_move2.set_text(str(pokemon_me.move2.name) + ' ' + str(pokemon_me.move2.pp_remain) + '/' + str(pokemon_me.move2.pp))
        self.btn_move3.set_text(str(pokemon_me.move3.name) + ' ' + str(pokemon_me.move3.pp_remain) + '/' + str(pokemon_me.move3.pp))
        self.btn_move4.set_text(str(pokemon_me.move4.name) + ' ' + str(pokemon_me.move4.pp_remain) + '/' + str(pokemon_me.move4.pp))

        color_move1 = self.color_mapping[pokemon_me.move1.type.lower()]
        self.btn_move1.colours['normal_border'] = color_move1
        self.btn_move1.colours['hovered_border'] = color_move1
        self.btn_move1.rebuild()
        color_move2 = self.color_mapping[pokemon_me.move2.type.lower()]
        self.btn_move2.colours['normal_border'] = color_move2
        self.btn_move2.colours['hovered_border'] = color_move2
        self.btn_move2.rebuild()
        color_move3 = self.color_mapping[pokemon_me.move3.type.lower()]
        self.btn_move3.colours['normal_border'] = color_move3
        self.btn_move3.colours['hovered_border'] = color_move3
        self.btn_move3.rebuild()
        color_move4 = self.color_mapping[pokemon_me.move4.type.lower()]
        self.btn_move4.colours['normal_border'] = color_move4
        self.btn_move4.colours['hovered_border'] = color_move4
        self.btn_move4.rebuild()
        if show_type_img:
            self.draw_types_moves_img(pokemon_me.move1.type, (self.screen_width * 0.645, self.screen_height * 0.79))
            self.draw_types_moves_img(pokemon_me.move2.type, (self.screen_width * 0.85, self.screen_height * 0.79))
            self.draw_types_moves_img(pokemon_me.move3.type, (self.screen_width * 0.645, self.screen_height * 0.975))
            self.draw_types_moves_img(pokemon_me.move4.type, (self.screen_width * 0.85, self.screen_height * 0.975))

        # Pokemon player enemy.
        # Move up/down several Pokemon on the screen for the correct position.
        if len(self.move_up) == 0:
            self.move_up = ['charizard', 'pidgeot', 'arcanine', 'machoke', 'machamp', 'rapidash', 'onix', 'exeggutor', 'kangaskhan', 'lapras', 'articuno', 'mewtwo', 'nidoqueen', 'nidoking',
                            'wartortle', 'venusaur', 'ninetales', 'fearow', 'pidgeotto', 'persian', 'alakazam', 'slowbro', 'dodrio', 'dewgong', 'hitmonlee', 'rhydon', 'snorlax', 'dragonite',
                            'moltres', 'victreebel']
        if len(self.move_down) == 0:
            self.move_down = ['rattata', 'bulbasaur', 'sandshrew', 'paras', 'diglett', 'ditto', 'omanyte', 'porygon', 'nidoran', 'spearow', 'jigglypuff', 'paras', 'growlithe', 'abra', 'grimer',
                              'krabby', 'exeggcute', 'cubone', 'kabuto']
        if self.pokemon_enemy_visible:
            pokemon_enemy_image = pygame.image.load('img_pokemon_battle_png/' + pokemon_enemy.name.lower() + '.png').convert_alpha()
            pokemon_enemy_image = pygame.transform.scale(pokemon_enemy_image, (pokemon_enemy_image.get_width() * 3, pokemon_enemy_image.get_height() * 3))
            if pokemon_enemy.name.lower() in self.move_up:
                self.screen.blit(pokemon_enemy_image, (self.screen_width * 0.73, self.screen_height * 0.015))
            elif pokemon_enemy.name.lower() in self.move_down:
                self.screen.blit(pokemon_enemy_image, (self.screen_width * 0.73, self.screen_height * 0.065))
            else:
                self.screen.blit(pokemon_enemy_image, (self.screen_width * 0.73, self.screen_height * 0.045))
        self.draw_types_pokemon_img(pokemon_enemy.type1, pokemon_enemy.type2, False)
        draw_name_enemy = self.font_name.render(pokemon_enemy.name, False, (0,0,0))
        self.screen.blit(draw_name_enemy, (self.screen_width * 0.11, self.screen_height * 0.08))

    def draw_types_pokemon_img(self, type1, type2, pokemon_me):
        """
        Draw on screen Pokemon types.
        :param type1: first Pokemon type.
        :param type2: second Pokemon type.
        :param pokemon_me: choose if me or enemy.
        :return:
        """
        type1_img = pygame.image.load('img/types/' + type1.lower() + '.png').convert_alpha()
        type1_img = pygame.transform.scale(type1_img, (type1_img.get_width() * 2, type1_img.get_height() * 2))
        if pokemon_me:
            self.screen.blit(type1_img, (self.screen_width * 0.86, self.screen_height * 0.5))
        else:
            self.screen.blit(type1_img, (self.screen_width * 0.3, self.screen_height * 0.105))
        if type2 != '':
            type2_img = pygame.image.load('img/types/' + type2.lower() + '.png').convert_alpha()
            type2_img = pygame.transform.scale(type2_img, (type2_img.get_width() * 2, type2_img.get_height() * 2))
            if pokemon_me:
                self.screen.blit(type2_img, (self.screen_width * 0.92, self.screen_height * 0.5))
            else:
                self.screen.blit(type2_img, (self.screen_width * 0.36, self.screen_height * 0.105))

    def renderHPBar(self, width, height, position, total_hp, actual_hp):
        """
        Draw Pokemon HP bar.
        :param width: HP bar width.
        :param height: HP bar height.
        :param position: HP bar position.
        :param total_hp: total Pokemon HP.
        :param actual_hp: actual Pokemon HP.
        :return:
        """
        percentage = float(actual_hp)/total_hp
        color = "green"
        if percentage < 0.5:
            color = "orange"
        if percentage < 0.2:
            color = "red"
        bar = pygame.Rect(position, (width*percentage, height))
        self.screen.fill(Color(color), bar)

    def draw_hp(self, hp_me, hp_enemy):
        """
        Draw HP bar for Pokemon in game.
        :param hp_me: HP player me.
        :param hp_enemy: Hp player enemy.
        :return:
        """
        self.renderHPBar(self.hp_img_enemy.get_width() * 0.62, self.hp_img_enemy.get_height() * 0.275, (self.screen_width * 0.178, self.screen_height * 0.16), self.model.enemy.team[0].battleHP, hp_enemy) # HP enemy
        self.renderHPBar(self.hp_img_me.get_width() * 0.6, self.hp_img_me.get_height() * 0.18, (self.screen_width * 0.732, self.screen_height * 0.552), self.model.me.team[0].battleHP, hp_me) # HP me
        draw_hp_number = self.font_hp.render(str(hp_me) + ' / ' + str(self.model.me.team[0].battleHP), False, (0,0,0))
        self.screen.blit(draw_hp_number, (self.screen_width * 0.75, self.screen_height * 0.62))

    def draw_types_moves_img(self, type, position):
        """
        Draw Pokemon types moves.
        :param type: Pokemon move type.
        :param position: type position on screen.
        :return:
        """
        type_img = pygame.image.load('img/types/' + type.lower() + '.png').convert_alpha()
        type_img = pygame.transform.scale(type_img, (self.screen_width * 0.042, self.screen_height * 0.023))
        self.screen.blit(type_img, position)

    def draw_team_choice_menu(self):
        """
        Draw the team choice menu on screen where the player can change Pokemon in battle.
        :return:
        """
        font_name = pygame.font.Font("fonts/VT323-Regular.ttf", 50)
        bg_team = pygame.image.load('img/bg_team.png').convert_alpha()
        bg_team = pygame.transform.scale(bg_team, (self.screen_width, self.screen_height))

        pokemon_list_menu_active, image_pokemon_active, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total =  self.create_pokemon_inbattle_menu(self.model.me.team[0].name, self.font_name, self.model.me.team[0].battleHP_actual, self.model.me.team[0].battleHP)
        pokemon_list_menu_deactive1, image_pokemon_deactive1, draw_pokemon_name1, draw_hp_number_actual1, draw_hp_number_total1 = self.create_pokemon_not_inbattle_menu(self.model.me.team[1].name, font_name, self.model.me.team[1].battleHP_actual, self.model.me.team[1].battleHP)
        pokemon_list_menu_deactive2, image_pokemon_deactive2, draw_pokemon_name2, draw_hp_number_actual2, draw_hp_number_total2 = self.create_pokemon_not_inbattle_menu(self.model.me.team[2].name, font_name, self.model.me.team[2].battleHP_actual, self.model.me.team[2].battleHP)
        pokemon_list_menu_deactive3, image_pokemon_deactive3, draw_pokemon_name3, draw_hp_number_actual3, draw_hp_number_total3 = self.create_pokemon_not_inbattle_menu(self.model.me.team[3].name, font_name, self.model.me.team[3].battleHP_actual, self.model.me.team[3].battleHP)
        pokemon_list_menu_deactive4, image_pokemon_deactive4, draw_pokemon_name4, draw_hp_number_actual4, draw_hp_number_total4 = self.create_pokemon_not_inbattle_menu(self.model.me.team[4].name, font_name, self.model.me.team[4].battleHP_actual, self.model.me.team[4].battleHP)
        pokemon_list_menu_deactive5, image_pokemon_deactive5, draw_pokemon_name5, draw_hp_number_actual5, draw_hp_number_total5 = self.create_pokemon_not_inbattle_menu(self.model.me.team[5].name, font_name, self.model.me.team[5].battleHP_actual, self.model.me.team[5].battleHP)

        text_description = pygame.font.Font("fonts/VT323-Regular.ttf", 80).render('Choose a Pokemon.', False, (0,0,0))
        text_exit = pygame.font.Font("fonts/VT323-Regular.ttf", 50).render('Exit', False, (255,255,255))
        self.rect_pokemon_list_menu_active = self.move_rect(pokemon_list_menu_active, -self.screen_width * 0.02, self.screen_height * 0.08)
        self.rect_pokemon_list_menu_deactive1 = self.move_rect(pokemon_list_menu_deactive1, self.screen_width * 0.352, self.screen_height * 0.023)
        self.rect_pokemon_list_menu_deactive2 = self.move_rect(pokemon_list_menu_deactive2, self.screen_width * 0.352, self.screen_height * 0.18)
        self.rect_pokemon_list_menu_deactive3 = self.move_rect(pokemon_list_menu_deactive3, self.screen_width * 0.352, self.screen_height * 0.335)
        self.rect_pokemon_list_menu_deactive4 = self.move_rect(pokemon_list_menu_deactive4, self.screen_width * 0.352, self.screen_height * 0.49)
        self.rect_pokemon_list_menu_deactive5 = self.move_rect(pokemon_list_menu_deactive5, self.screen_width * 0.352, self.screen_height * 0.645)
        self.rect_text_exit = self.move_rect(text_exit, self.screen_width * 0.855, self.screen_height * 0.875)

        self.screen.blit(bg_team, (0, 0))
        self.screen.blit(pokemon_list_menu_active, (-self.screen_width * 0.02, self.screen_height * 0.08))
        self.screen.blit(image_pokemon_active, (self.screen_width * 0.03, self.screen_height * 0.17))
        self.screen.blit(draw_pokemon_name, (self.screen_width * 0.173, self.screen_height * 0.22))
        self.screen.blit(draw_hp_number_actual, (self.screen_width * 0.195, self.screen_height * 0.4))
        self.screen.blit(draw_hp_number_total, (self.screen_width * 0.28, self.screen_height * 0.4))
        self.screen.blit(pokemon_list_menu_deactive1, (self.screen_width * 0.352, self.screen_height * 0.023))
        self.screen.blit(image_pokemon_deactive1, (self.screen_width * 0.40, self.screen_height * 0.056))
        self.screen.blit(draw_pokemon_name1, (self.screen_width * 0.54, self.screen_height * 0.07))
        self.screen.blit(draw_hp_number_actual1, (self.screen_width * 0.84, self.screen_height * 0.13))
        self.screen.blit(draw_hp_number_total1, (self.screen_width * 0.92, self.screen_height * 0.13))
        self.screen.blit(pokemon_list_menu_deactive2, (self.screen_width * 0.352, self.screen_height * 0.18))
        self.screen.blit(image_pokemon_deactive2, (self.screen_width * 0.40, self.screen_height * 0.215))
        self.screen.blit(draw_pokemon_name2, (self.screen_width * 0.54, self.screen_height * 0.225))
        self.screen.blit(draw_hp_number_actual2, (self.screen_width * 0.84, self.screen_height * 0.285))
        self.screen.blit(draw_hp_number_total2, (self.screen_width * 0.92, self.screen_height * 0.285))
        self.screen.blit(pokemon_list_menu_deactive3, (self.screen_width * 0.352, self.screen_height * 0.335))
        self.screen.blit(image_pokemon_deactive3, (self.screen_width * 0.40, self.screen_height * 0.37))
        self.screen.blit(draw_pokemon_name3, (self.screen_width * 0.54, self.screen_height * 0.38))
        self.screen.blit(draw_hp_number_actual3, (self.screen_width * 0.84, self.screen_height * 0.44))
        self.screen.blit(draw_hp_number_total3, (self.screen_width * 0.92, self.screen_height * 0.44))
        self.screen.blit(pokemon_list_menu_deactive4, (self.screen_width * 0.352, self.screen_height * 0.49))
        self.screen.blit(image_pokemon_deactive4, (self.screen_width * 0.40, self.screen_height * 0.525))
        self.screen.blit(draw_pokemon_name4, (self.screen_width * 0.54, self.screen_height * 0.535))
        self.screen.blit(draw_hp_number_actual4, (self.screen_width * 0.84, self.screen_height * 0.595))
        self.screen.blit(draw_hp_number_total4, (self.screen_width * 0.92, self.screen_height * 0.595))
        self.screen.blit(pokemon_list_menu_deactive5, (self.screen_width * 0.352, self.screen_height * 0.645))
        self.screen.blit(image_pokemon_deactive5, (self.screen_width * 0.40, self.screen_height * 0.68))
        self.screen.blit(draw_pokemon_name5, (self.screen_width * 0.54, self.screen_height * 0.69))
        self.screen.blit(draw_hp_number_actual5, (self.screen_width * 0.84, self.screen_height * 0.75))
        self.screen.blit(draw_hp_number_total5, (self.screen_width * 0.92, self.screen_height * 0.75))
        self.screen.blit(text_description, (self.screen_width * 0.05, self.screen_height * 0.87))
        self.screen.blit(text_exit, (self.screen_width * 0.855, self.screen_height * 0.875))

    def create_pokemon_not_inbattle_menu(self, pokemon_name, font_name, hp_actual, hp_total):
        """
        Create Pokemon image with its name and actual HP for team Pokemon not in battle.
        :param pokemon_name: Pokemon name.
        :param font_name: font name.
        :param hp_actual: Pokemon HP actual.
        :param hp_total: Pokemon HP total.
        :return: Every Pokemon info to draw on screen.
        """
        pokemon_list_menu_deactive = pygame.image.load('img/pokemon_team.png').convert_alpha()
        pokemon_list_menu_deactive = pygame.transform.scale(pokemon_list_menu_deactive, (self.screen_width * 0.66, self.screen_height * 0.18))
        image_pokemon_deactive = pygame.image.load('img_pokemon_battle_png/' + pokemon_name.lower() + '.png').convert_alpha()
        image_pokemon_deactive = pygame.transform.scale(image_pokemon_deactive, (self.screen_width * 0.13, self.screen_height * 0.13))
        draw_pokemon_name = font_name.render(pokemon_name, False, (255,255,255))
        draw_hp_number_actual = font_name.render(str(hp_actual), False, (255,255,255))
        draw_hp_number_total = font_name.render(str(hp_total), False, (255,255,255))
        return pokemon_list_menu_deactive, image_pokemon_deactive, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total

    def create_pokemon_inbattle_menu(self, pokemon_name, font_name, hp_actual, hp_total):
        """
        Create Pokemon image with its name and actual HP for Pokemon in battle.
        :param pokemon_name: Pokemon name.
        :param font_name: font name.
        :param hp_actual: Pokemon HP actual.
        :param hp_total: Pokemon HP total.
        :return: Every Pokemon info to draw on screen.
        """
        pokemon_list_menu_active = pygame.image.load('img/my_pokemon.png').convert_alpha()
        pokemon_list_menu_active = pygame.transform.scale(pokemon_list_menu_active, (self.screen_width * 0.4, self.screen_height * 0.42))
        image_pokemon_active = pygame.image.load('img_pokemon_battle_png/' + pokemon_name.lower() + '.png').convert_alpha()
        image_pokemon_active = pygame.transform.scale(image_pokemon_active, (self.screen_width * 0.15, self.screen_height * 0.15))
        draw_pokemon_name = font_name.render(pokemon_name, False, (255,255,255))
        draw_hp_number_actual = font_name.render(str(hp_actual), False, (255,255,255))
        draw_hp_number_total = font_name.render(str(hp_total), False, (255,255,255))
        return pokemon_list_menu_active, image_pokemon_active, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total

    def draw_HP_pokemon_choice_menu(self):
        """
        Draw Pokemon HP in choice menu.
        :return:
        """
        self.renderHPBar(self.screen_width * 0.209, self.screen_height * 0.022, (self.screen_width * 0.129, self.screen_height * 0.373), self.model.me.team[0].battleHP, self.model.me.team[0].battleHP_actual) # HP actual pokemon
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.095), self.model.me.team[1].battleHP, self.model.me.team[1].battleHP_actual) # HP pokemon 1
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.252), self.model.me.team[2].battleHP, self.model.me.team[2].battleHP_actual) # HP pokemon 2
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.408), self.model.me.team[3].battleHP, self.model.me.team[3].battleHP_actual) # HP pokemon 3
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.563), self.model.me.team[4].battleHP, self.model.me.team[4].battleHP_actual) # HP pokemon 4
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.718), self.model.me.team[5].battleHP, self.model.me.team[5].battleHP_actual) # HP pokemon 5

    def move_rect(self, surface, posx, posy):
        """
        Move render surface on screen.
        :param surface: surface to move.
        :param posx: new x coordinate.
        :param posy: new y coordinate.
        :return: Surface in new position.
        """
        play_game_rect = surface.get_rect()
        play_game_rect.x = posx
        play_game_rect.y = posy
        return play_game_rect

    def draw_fundamental_parts(self, draw_btn_change_pokemon):
        """
        Draw some objects on screen when player waiting for an opponent.
        :param draw_btn_change_pokemon: Check if draw Change Pokemon button.
        :return:
        """
        self.screen.fill(BG)
        self.draw_bg()
        self.draw_battle_description(self.description_battle)
        self.draw_button(draw_btn_change_pokemon)

    def update_battle_window(self, show_button, show_type_img):
        """
        Update battle window to show/hide objects on screen.
        :param show_button: choose if show/hide buttons.
        :param show_type_img: choose if show Pokemon move type images.
        :return:
        """
        self.screen.fill(BG)
        self.draw_bg()
        if self.start_battle:
            self.description_battle = str(self.model.me.team[0].name) + ' it\'s your turn.'
        self.draw_battle_description(self.description_battle)
        if not self.draw_button_battle:
            self.draw_button(True)
            self.draw_button_moves()
            self.draw_button_battle = True
        if show_button:
            self.btn_change_pokemon.show()
            self.btn_quit.show()
            self.btn_move1.show()
            self.btn_move2.show()
            self.btn_move3.show()
            self.btn_move4.show()
        else:
            self.hide_buttons()
        self.draw_pokemon(self.model.me.team[0], self.model.enemy.team[0], show_type_img)

    def hide_buttons(self):
        """
        Hide buttons.
        :return:
        """
        self.btn_change_pokemon.hide()
        self.btn_quit.hide()
        self.btn_move1.hide()
        self.btn_move2.hide()
        self.btn_move3.hide()
        self.btn_move4.hide()

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

    def exit_battle_operations(self):
        """
        Necessary operations before exit from battle and close the game.
        :return:
        """
        utils.reset_team_stats(self.model.me)
        utils.reset_team_stats(self.model.enemy)
        self.model.enemy.team = []
        self.model.enemy.name = ''
        self.run = False

    def basic_events(self):
        """
        Handle basic events as they happen
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element.most_specific_combined_id == self.btn_quit.most_specific_combined_id:
                    self.exit_battle = True
            self.manager.process_events(event)

    def update_manager_and_display(self):
        """
        Update manager to display objects on screen.
        :return:
        """
        time_delta = self.clock.tick(self.FPS)/1000.0
        self.manager.update(time_delta)

        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def wait(self, wait, show_button, show_type_img):
        """
        It allows waiting for visualize animations on screen.
        :param wait: time to wait.
        :param show_button: choose if show/hide buttons.
        :param show_type_img: choose if show Pokemon move type images.
        :return:
        """
        k = 0
        while k < wait:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(show_button, show_type_img)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()
            k += 1

    def start_battle_animations(self, trainer_me, trainer_enemy, show_button, show_type_img):
        """
        Show initials animations of battle.
        :param trainer_me: frames trainer me to show.
        :param trainer_enemy: frames trainer enemy to show.
        :param show_button: choose if show/hide buttons.
        :param show_type_img: choose if show Pokemon move type images.
        :return:
        """
        k = 0
        wait_frame = 30
        while k < wait_frame:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(show_button, show_type_img)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
            trainer_img = pygame.transform.scale(trainer_me[k // 6], (trainer_me[k // 6].get_width() * 4, trainer_me[k // 6].get_height() * 4)).convert_alpha()
            self.screen.blit(trainer_img, (-self.screen_width * 0.02, self.screen_height * 0.445))
            trainer_img_enemy = pygame.transform.scale(trainer_enemy[k // 10], (trainer_enemy[k // 10].get_width() * 3, trainer_enemy[k // 10].get_height() * 3)).convert_alpha()
            self.screen.blit(trainer_img_enemy, (self.screen_width * 0.85, self.screen_height * 0.04))

            self.update_manager_and_display()
            k += 1

    def pokeball_animations(self, wait_frame, show_button, show_type_img, open_pokeball, pokemon_me, pokemon_enemy, animation_me, animation_enemy):
        """
        Pokeball animations on screen.
        :param wait_frame: frame to wait to visualize animations.
        :param show_button: choose if show/hide buttons.
        :param show_type_img: choose if show Pokemon move type images.
        :param open_pokeball: choose if open pokeball animation or the close one.
        :param pokemon_me: Pokemon player me in game.
        :param pokemon_enemy: Pokemon player enemy in game.
        :param animation_me: choose if animation Player me.
        :param animation_enemy: choose if animation Player enemy.
        :return:
        """
        k = 0
        while k < wait_frame:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(show_button, show_type_img)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
            if animation_enemy:
                pokeball_type = pokemon_enemy.pokeball
                filename = utils.read_pokeball(open_pokeball, pokeball_type)
                pokeball_image_enemy = pygame.image.load('img/pokeballs/' + filename + '.png').convert_alpha()
                pokeball_image_enemy = pygame.transform.flip(pokeball_image_enemy, True, False)
                pokeball_image_enemy = pygame.transform.scale(pokeball_image_enemy, (pokeball_image_enemy.get_width() * 2, pokeball_image_enemy.get_height() * 2)).convert_alpha()
                if open_pokeball:
                    self.screen.blit(pokeball_image_enemy, (self.screen_width * 0.82, self.screen_height * 0.22))
                else:
                    self.screen.blit(pokeball_image_enemy, (self.screen_width * 0.82, self.screen_height * 0.23))

            if animation_me:
                pokeball_type = pokemon_me.pokeball
                filename = utils.read_pokeball(open_pokeball, pokeball_type)
                pokeball_image = pygame.image.load('img/pokeballs/' + filename + '.png').convert_alpha()
                pokeball_image = pygame.transform.scale(pokeball_image, (pokeball_image.get_width() * 3, pokeball_image.get_height() * 3)).convert_alpha()
                self.screen.blit(pokeball_image, (self.screen_width * 0.22, self.screen_height * 0.68))

            self.update_manager_and_display()
            k += 1

    def explosion_animations(self, show_button, show_type_img, animation_pokemon_me):
        """
        Explosion animations on Pokemon when a another Pokemon attack.
        :param show_button: choose if show/hide buttons.
        :param show_type_img: choose if show Pokemon move type images.
        :param animation_pokemon_me: choose if visualize animation on Pokemon player me or enemy.
        :return:
        """
        k = 0
        wait_frame = 39
        while k < wait_frame:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(show_button, show_type_img)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
            if animation_pokemon_me:
                explosion = pygame.transform.scale(self.explosion_sheet[k], (self.explosion_sheet[k].get_width() * 1.5, self.explosion_sheet[k].get_height() * 1.5)).convert_alpha()
                self.screen.blit(explosion, (self.screen_width * 0.15, self.screen_height * 0.58))
            else:
                self.screen.blit(self.explosion_sheet[k], (self.screen_width * 0.79, self.screen_height * 0.15))

            self.update_manager_and_display()
            k += 1

    def reduce_hp_bar(self, show_button, show_type_img, player_attacker, reduced_hp):
        """
        Animation tp reduce HP bar of a Pokemon.
        :param show_button: choose if show/hide buttons.
        :param show_type_img: choose if show Pokemon move type images.
        :param player_attacker: choose if get HP player me or enemy.
        :param reduced_hp: damage of attack received.
        :return:
        """
        if player_attacker:
            actual_hp = self.model.enemy.team[0].battleHP_actual
        else:
            actual_hp = self.model.me.team[0].battleHP_actual
        k = 0
        reduced_hp = abs(reduced_hp)
        while k < reduced_hp:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(show_button, show_type_img)
            if player_attacker:
                self.draw_hp(self.model.me.team[0].battleHP_actual, actual_hp + reduced_hp - k)
            else:
                self.draw_hp(actual_hp + reduced_hp - k, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()
            k += 1

    def change_pokemon(self):
        """
        Change Pokemon on screen and show the other one that is chosen.
        :return: [pokemon_changed, pokemon_withdrawn, new_pokemon_active] = Returns if Pokemon is changed and if so return
        the Pokemon withdrawn and the new one, else None.
        """
        self.screen.fill(BG)
        self.hide_buttons()
        self.draw_team_choice_menu()
        self.draw_HP_pokemon_choice_menu()

        pokemon_changed = False
        pokemon_withdrawn = None
        new_pokemon_active = None

        for event in pygame.event.get():
            if self.rect_pokemon_list_menu_active.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[0].battleHP_actual > 0:
                        self.change_pokemon_menu = False
            if self.rect_pokemon_list_menu_deactive1.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[1].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[1]
                        self.special_moves_me = None
                        self.count_move_me = 0
                        self.model.me.swap_position(0, 1)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive2.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[2].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[2]
                        self.special_moves_me = None
                        self.count_move_me = 0
                        self.model.me.swap_position(0, 2)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive3.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[3].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[3]
                        self.special_moves_me = None
                        self.count_move_me = 0
                        self.model.me.swap_position(0, 3)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive4.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[4].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[4]
                        self.special_moves_me = None
                        self.count_move_me = 0
                        self.model.me.swap_position(0, 4)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive5.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[5].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[5]
                        self.special_moves_me = None
                        self.count_move_me = 0
                        self.model.me.swap_position(0, 5)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
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
            self.basic_events()

            if self.exit_battle:
                self.exit_battle_operations()
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

            self.update_manager_and_display()

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
            self.basic_events()

            if self.exit_battle:
                self.exit_battle_operations()
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

            self.update_manager_and_display()

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
            self.basic_events()

            if self.exit_battle:
                self.exit_battle_operations()
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
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()

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
            self.basic_events()

            if self.exit_battle:
                self.exit_battle_operations()
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
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()

    def connection_lost_waiting(self, wait):
        """
        Remain in game and waiting a new player if connection is lost with the enemy.
        :param wait: time to wait.
        :return:
        """
        k = 0
        while k < wait:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.draw_fundamental_parts(False)

            self.update_manager_and_display()
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

            self.screen.fill(BG)
            message_server_off = pygame.font.Font("fonts/VT323-Regular.ttf", 60).render('Start the server for multiplayer mode', False, (0,0,0))
            self.screen.blit(message_server_off, (self.screen_width * 0.17, self.screen_height * 0.45))

            self.update_manager_and_display()
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
        self.pokeball_animations(10, False, False, False, self.model.me.team[0], self.model.enemy.team[0], False, True)
        self.pokeball_animations(10, False, False, True, self.model.me.team[0], self.model.enemy.team[0], False, True)
        self.pokemon_enemy_visible = True

    def read_players_attack(self, move_me):
        """
        Read players attack and start the game turn.
        :param move_me: move player me.
        :return:
        """
        prob_accuracy = random.random() * 100
        critic_value = random.uniform(0.85, 1.0)
        self.find_enemy_move(True, move_me, prob_accuracy, critic_value, None, None)
        if self.move_enemy_found and self.enemy_move_data:
            self.read_data_moves()
            game_multiplayer.checks_2_turns_attack(self, move_me, self.move_enemy, self.prob_accuracy, self.critic_value)

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
                self.wait(30, False, False)

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
                    self.exit_battle_operations()
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
                                        self.pokeball_animations(10, False, False, False, self.model.me.team[0], self.model.enemy.team[0], True, False)
                                        self.pokeball_animations(10, False, False, True, self.model.me.team[0], self.model.enemy.team[0], True, False)
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
                                    self.find_enemy_move(False, None, None, None, self.pokemon_withdrawn, self.new_pokemon_active)
                                    # check if enemy move and data are found.
                                    if self.move_enemy_found and self.enemy_move_data:
                                        self.read_data_moves()
                                        game_multiplayer.checks_2_turns_attack(self, None, self.move_enemy, self.prob_accuracy, self.critic_value)
                                # check if Pokemon of player me do a special move and calculate its values.
                                elif self.special_moves_me is not None:
                                    prob_accuracy = random.random() * 100
                                    critic_value = random.uniform(0.85, 1.0)
                                    self.find_enemy_move(True, self.special_moves_me, prob_accuracy, critic_value, None, None)
                                    # check if enemy move and data are found.
                                    if self.move_enemy_found and self.enemy_move_data:
                                        self.read_data_moves()
                                        game_multiplayer.checks_2_turns_attack(self, self.special_moves_me, self.move_enemy, self.prob_accuracy, self.critic_value)
                                else:
                                    # todo check function
                                    if not self.change_pokemon_menu:
                                        # check if the Game is started and if so run the first animations.
                                        if start_animations:
                                            self.start_battle_animations(trainer_me, trainer_enemy, False, False)
                                            self.pokeball_animations(10, False, False, False, self.model.me.team[0], self.model.enemy.team[0], True, True)
                                            self.pokeball_animations(10, False, False, True, self.model.me.team[0], self.model.enemy.team[0], True, True)
                                            start_animations = False
                                            self.pokemon_me_visible = True
                                            self.pokemon_enemy_visible = True
                                        # normal execution of the Game.
                                        else:
                                            self.update_battle_window(True, True)
                                            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
                                        self.start_battle = False
                                        self.description_battle = 'What will ' + self.model.me.team[0].name + ' do?'
                                    # check if the change Pokemon menu is active.
                                    else:
                                        change_pokemon, self.pokemon_withdrawn, self.new_pokemon_active = self.change_pokemon()
                                        # Check if user change Pokemon and if so the animation start.
                                        if change_pokemon:
                                            self.pokemon_me_visible = False
                                            self.pokeball_animations(10, False, False, False, self.model.me.team[0], self.model.enemy.team[0], True, False)
                                            self.pokeball_animations(10, False, False, True, self.model.me.team[0], self.model.enemy.team[0], True, False)
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

            self.update_manager_and_display()
        pygame.quit()








