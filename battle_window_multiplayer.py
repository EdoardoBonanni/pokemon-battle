from models.Model import Model
import pygame
from pygame.locals import *
import pygame_gui
from utility import utils
from utility import game_multiplayer
from connection.network import Network
from copy import deepcopy
import ast, os, random

#define colours
BG_GREEN = (144, 201, 120)
BG = (224, 235, 235)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

class battle_window_multiplayer:
    def __init__(self, model: Model, width, height, pos_x, pos_y):
        self.model = model
        self.names = None
        self.i = 0
        self.screen_width = 1300
        self.screen_height = int(1300 * 0.7)
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)

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

    def draw_button_moves(self):
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
        # pokemon me
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
            self.draw_types_img(pokemon_me.move1.type, (self.screen_width * 0.645, self.screen_height * 0.788))
            self.draw_types_img(pokemon_me.move2.type, (self.screen_width * 0.85, self.screen_height * 0.788))
            self.draw_types_img(pokemon_me.move3.type, (self.screen_width * 0.645, self.screen_height * 0.975))
            self.draw_types_img(pokemon_me.move4.type, (self.screen_width * 0.85, self.screen_height * 0.975))

        # pokemon enemy
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
        draw_name_enemy = self.font_name.render(pokemon_enemy.name, False, (0,0,0))
        self.screen.blit(draw_name_enemy, (self.screen_width * 0.11, self.screen_height * 0.08))

    def renderHPBar(self, bar_size, height, position, total_hp, actual_hp):
        percentage = float(actual_hp)/total_hp
        color = "green"
        if percentage < 0.5:
            color = "orange"
        if percentage < 0.2:
            color = "red"
        bar = pygame.Rect(position, (bar_size*percentage, height))
        self.screen.fill(Color(color), bar)

    def draw_hp(self, hp_me, hp_enemy):
        self.renderHPBar(self.hp_img_enemy.get_width() * 0.62, self.hp_img_enemy.get_height() * 0.275, (self.screen_width * 0.178, self.screen_height * 0.16), self.model.enemy.team[0].battleHP, hp_enemy) # HP enemy
        self.renderHPBar(self.hp_img_me.get_width() * 0.6, self.hp_img_me.get_height() * 0.18, (self.screen_width * 0.732, self.screen_height * 0.552), self.model.me.team[0].battleHP, hp_me) # HP me
        draw_hp_number = self.font_hp.render(str(hp_me) + ' / ' + str(self.model.me.team[0].battleHP), False, (0,0,0))
        self.screen.blit(draw_hp_number, (self.screen_width * 0.75, self.screen_height * 0.62))

    def draw_types_img(self, type, position):
        type_img = pygame.image.load('img/types/' + type.lower() + '.png').convert_alpha()
        type_img = pygame.transform.scale(type_img, (self.screen_width * 0.045, self.screen_height * 0.025))
        self.screen.blit(type_img, position)

    def draw_pokemon_choose_menu(self):
        font_name = pygame.font.Font("fonts/VT323-Regular.ttf", 50)
        bg_team = pygame.image.load('img/bg_team.png').convert_alpha()
        bg_team = pygame.transform.scale(bg_team, (self.screen_width, self.screen_height))

        pokemon_list_menu_active, image_pokemon_active, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total =  self.draw_pokemon_active_menu(self.model.me.team[0].name, self.font_name, self.model.me.team[0].battleHP_actual, self.model.me.team[0].battleHP)
        pokemon_list_menu_deactive1, image_pokemon_deactive1, draw_pokemon_name1, draw_hp_number_actual1, draw_hp_number_total1 = self.draw_pokemon_deactive_menu(self.model.me.team[1].name, font_name, self.model.me.team[1].battleHP_actual, self.model.me.team[1].battleHP)
        pokemon_list_menu_deactive2, image_pokemon_deactive2, draw_pokemon_name2, draw_hp_number_actual2, draw_hp_number_total2 = self.draw_pokemon_deactive_menu(self.model.me.team[2].name, font_name, self.model.me.team[2].battleHP_actual, self.model.me.team[2].battleHP)
        pokemon_list_menu_deactive3, image_pokemon_deactive3, draw_pokemon_name3, draw_hp_number_actual3, draw_hp_number_total3 = self.draw_pokemon_deactive_menu(self.model.me.team[3].name, font_name, self.model.me.team[3].battleHP_actual, self.model.me.team[3].battleHP)
        pokemon_list_menu_deactive4, image_pokemon_deactive4, draw_pokemon_name4, draw_hp_number_actual4, draw_hp_number_total4 = self.draw_pokemon_deactive_menu(self.model.me.team[4].name, font_name, self.model.me.team[4].battleHP_actual, self.model.me.team[4].battleHP)
        pokemon_list_menu_deactive5, image_pokemon_deactive5, draw_pokemon_name5, draw_hp_number_actual5, draw_hp_number_total5 = self.draw_pokemon_deactive_menu(self.model.me.team[5].name, font_name, self.model.me.team[5].battleHP_actual, self.model.me.team[5].battleHP)

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

    def draw_pokemon_deactive_menu(self, pokemon_name, font_name, hp_actual, hp_total):
        pokemon_list_menu_deactive = pygame.image.load('img/pokemon_team.png').convert_alpha()
        pokemon_list_menu_deactive = pygame.transform.scale(pokemon_list_menu_deactive, (self.screen_width * 0.66, self.screen_height * 0.18))
        image_pokemon_deactive = pygame.image.load('img_pokemon_battle_png/' + pokemon_name.lower() + '.png').convert_alpha()
        image_pokemon_deactive = pygame.transform.scale(image_pokemon_deactive, (self.screen_width * 0.13, self.screen_height * 0.13))
        draw_pokemon_name = font_name.render(pokemon_name, False, (255,255,255))
        draw_hp_number_actual = font_name.render(str(hp_actual), False, (255,255,255))
        draw_hp_number_total = font_name.render(str(hp_total), False, (255,255,255))
        return pokemon_list_menu_deactive, image_pokemon_deactive, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total

    def draw_pokemon_active_menu(self, pokemon_name, font_name, hp_actual, hp_total):
        pokemon_list_menu_active = pygame.image.load('img/my_pokemon.png').convert_alpha()
        pokemon_list_menu_active = pygame.transform.scale(pokemon_list_menu_active, (self.screen_width * 0.4, self.screen_height * 0.42))
        image_pokemon_active = pygame.image.load('img_pokemon_battle_png/' + pokemon_name.lower() + '.png').convert_alpha()
        image_pokemon_active = pygame.transform.scale(image_pokemon_active, (self.screen_width * 0.15, self.screen_height * 0.15))
        draw_pokemon_name = font_name.render(pokemon_name, False, (255,255,255))
        draw_hp_number_actual = font_name.render(str(hp_actual), False, (255,255,255))
        draw_hp_number_total = font_name.render(str(hp_total), False, (255,255,255))
        return pokemon_list_menu_active, image_pokemon_active, draw_pokemon_name, draw_hp_number_actual, draw_hp_number_total

    def draw_HP_pokemon_choose_menu(self):
        self.renderHPBar(self.screen_width * 0.209, self.screen_height * 0.022, (self.screen_width * 0.129, self.screen_height * 0.373), self.model.me.team[0].battleHP, self.model.me.team[0].battleHP_actual) # HP actual pokemon
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.095), self.model.me.team[1].battleHP, self.model.me.team[1].battleHP_actual) # HP pokemon 1
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.252), self.model.me.team[2].battleHP, self.model.me.team[2].battleHP_actual) # HP pokemon 2
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.408), self.model.me.team[3].battleHP, self.model.me.team[3].battleHP_actual) # HP pokemon 3
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.563), self.model.me.team[4].battleHP, self.model.me.team[4].battleHP_actual) # HP pokemon 4
        self.renderHPBar(self.screen_width * 0.2, self.screen_height * 0.022, (self.screen_width * 0.77, self.screen_height * 0.718), self.model.me.team[5].battleHP, self.model.me.team[5].battleHP_actual) # HP pokemon 5

    def move_rect(self, draw, posx, posy):
        play_game_rect = draw.get_rect()
        play_game_rect.x = posx
        play_game_rect.y = posy
        return play_game_rect

    def draw_fondamental_parts(self, draw_btn_change_pokemon):
        self.screen.fill(BG)
        self.draw_bg()
        self.draw_battle_description(self.description_battle)
        self.draw_button(draw_btn_change_pokemon)

    def update_battle_window(self, show_button, show_type_img):
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
            self.btn_change_pokemon.hide()
            self.btn_quit.hide()
            self.btn_move1.hide()
            self.btn_move2.hide()
            self.btn_move3.hide()
            self.btn_move4.hide()
        self.draw_pokemon(self.model.me.team[0], self.model.enemy.team[0], show_type_img)

    def reset_buttons(self):
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

    def start_battle_animations(self, trainer_me, trainer_enemy, update_button, show_type_img):
        k = 0
        wait_frame = 30
        while k < wait_frame:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(update_button, show_type_img)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
            trainer_img = pygame.transform.scale(trainer_me[k // 6], (trainer_me[k // 6].get_width() * 4, trainer_me[k // 6].get_height() * 4)).convert_alpha()
            self.screen.blit(trainer_img, (-self.screen_width * 0.02, self.screen_height * 0.445))
            trainer_img_enemy = pygame.transform.scale(trainer_enemy[k // 10], (trainer_enemy[k // 10].get_width() * 3, trainer_enemy[k // 10].get_height() * 3)).convert_alpha()
            self.screen.blit(trainer_img_enemy, (self.screen_width * 0.85, self.screen_height * 0.04))

            self.update_manager_and_display()
            k += 1

    def pokeball_animations(self, wait_frame, update_button, show_type_img, open_pokeball, pokemon_me, pokemon_enemy, animation_me, animation_enemy):
        k = 0
        while k < wait_frame:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(update_button, show_type_img)
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

    def explosion_animations(self, update_button, show_type_img, animation_pokemon_me):
        k = 0
        wait_frame = 39
        while k < wait_frame:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(update_button, show_type_img)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
            if animation_pokemon_me:
                explosion = pygame.transform.scale(self.explosion_sheet[k], (self.explosion_sheet[k].get_width() * 1.5, self.explosion_sheet[k].get_height() * 1.5)).convert_alpha()
                self.screen.blit(explosion, (self.screen_width * 0.15, self.screen_height * 0.58))
            else:
                self.screen.blit(self.explosion_sheet[k], (self.screen_width * 0.79, self.screen_height * 0.15))

            self.update_manager_and_display()
            k += 1

    def reduce_hp_bar(self, update_button, show_type_img, player_attacker, reduced_hp):
        if player_attacker:
            actual_hp = self.model.enemy.team[0].battleHP_actual
        else:
            actual_hp = self.model.me.team[0].battleHP_actual
        k = 0
        reduced_hp = abs(reduced_hp)
        while k < reduced_hp:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(update_button, show_type_img)
            if player_attacker:
                self.draw_hp(self.model.me.team[0].battleHP_actual, actual_hp + reduced_hp - k)
            else:
                self.draw_hp(actual_hp + reduced_hp - k, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()
            k += 1

    def change_pokemon(self):
        self.screen.fill(BG)
        self.btn_change_pokemon.hide()
        self.btn_quit.hide()
        self.btn_move1.hide()
        self.btn_move2.hide()
        self.btn_move3.hide()
        self.btn_move4.hide()
        self.draw_pokemon_choose_menu()
        self.draw_HP_pokemon_choose_menu()

        pokemon_changed = False
        pokemon_withdrawn = None
        new_pokemon_active = None

        for event in pygame.event.get():
            if self.rect_pokemon_list_menu_active.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.model.me.team[0].battleHP_actual > 0:
                        self.change_pokemon_menu = False
            if self.rect_pokemon_list_menu_deactive1.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.model.me.team[1].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[1]
                        self.model.me.swap_position(0, 1)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive2.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.model.me.team[2].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[2]
                        self.model.me.swap_position(0, 2)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive3.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.model.me.team[3].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[3]
                        self.model.me.swap_position(0, 3)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive4.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.model.me.team[4].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[4]
                        self.model.me.swap_position(0, 4)
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_pokemon_list_menu_deactive5.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.model.me.team[5].battleHP_actual > 0:
                        if self.model.me.team[0].battleHP_actual != 0:
                            self.pokemon_changed_not_fainted = True
                        utils.reset_stats(self.model.me.team[0])
                        self.model.me.swap_position(0, 5)
                        pokemon_withdrawn = self.model.me.team[0]
                        new_pokemon_active = self.model.me.team[5]
                        self.change_pokemon_menu = False
                        pokemon_changed = True
            if self.rect_text_exit.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.model.me.team[0].battleHP_actual > 0:
                        self.change_pokemon_menu = False
        self.description_battle = 'What will ' + self.model.me.team[0].name + ' do?'
        return pokemon_changed, pokemon_withdrawn, new_pokemon_active

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
                    data = {'type': 'send_player_name',
                            'player_name': str(self.model.me.name)
                            }
                    data_str = str(data)
                    self.net.send(data_str)
                    name_send = True

                if message.both_went() and not self.name_enemy_found:
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data['type'] == 'send_player_name':
                        self.model.enemy.name = str(data['player_name'])
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
                    if data['type'] == 'send_team':
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon0'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon1'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon2'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon3'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon4'])]))
                        self.model.enemy.add_pokemon(deepcopy(self.model.pokedex.listPokemon[str(data['pokemon5'])]))
                        self.team_enemy_found = True
                        self.net.send('reset')

                if self.name_enemy_found:
                    k = k + 1

            self.description_battle = 'Configuration phase ...'
            self.draw_fondamental_parts(False)

            self.update_manager_and_display()

    def find_enemy_move(self, attack, move, prob_accuracy, critic_value, pokemon_withdrawn, new_pokemon_active):
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
                    if attack:
                        if self.special_moves_me:
                            special_move = str(self.special_moves_me)
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
                    self.net.send(data_str)
                    move_send = True

                if message.both_went() and not self.move_enemy_found:
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data['type'] == 'attack':
                        self.enemy_move_data = deepcopy(data)
                        self.enemy_use_attack = True
                        self.move_enemy_found = True
                        self.net.send('reset')
                    elif data['type'] == 'change_pokemon':
                        self.enemy_move_data = deepcopy(data)
                        self.move_enemy_found = True
                        self.net.send('reset')

                if self.move_enemy_found:
                    k = k + 1

            self.description_battle = 'Waiting for enemy move ...'
            self.update_battle_window(False, False)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()

    def find_pokemon_fainted(self, pokemon_withdrawn, new_pokemon_active):
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
                    if pokemon_withdrawn and new_pokemon_active:
                        data = {'type': 'change_pokemon_fainted',
                                'pokemon_withdrawn': str(pokemon_withdrawn.name),
                                'new_pokemon_active': str(new_pokemon_active.name)
                                }
                    else:
                        data = {'type': 'change_pokemon_fainted',
                                'pokemon_withdrawn': 'None',
                                'new_pokemon_active': 'None'
                                }
                    data_str = str(data)
                    self.net.send(data_str)
                    pokemon_fainted_send = True

                if message.both_went() and not self.pokemon_fainted_found:
                    other_player = (self.player + 1) % 2
                    data_str = message.get_data(other_player)
                    data = ast.literal_eval(data_str)
                    if data['type'] == 'change_pokemon_fainted':
                        self.pokemon_fainted_data = deepcopy(data)
                        self.pokemon_fainted_found = True
                        self.net.send('reset')

                if self.move_enemy_found:
                    k = k + 1

            self.description_battle = 'Waiting for enemy move ...'
            self.update_battle_window(False, False)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()

    def connection_lost_waiting(self, wait):
        k = 0
        while k < wait:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.draw_fondamental_parts(False)

            self.update_manager_and_display()
            k += 1

    def wait(self, wait, update_button, show_type_img):
        k = 0
        while k < wait:
            self.clock.tick(self.FPS)
            self.basic_events()

            self.update_battle_window(update_button, show_type_img)
            self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)

            self.update_manager_and_display()
            k += 1

    def read_data(self):
        if self.enemy_use_attack:
            if self.enemy_move_data['type'] == 'attack':
                # pokemon_active_str = str(self.enemy_move_data['pokemon_active'])
                # pokemon_active = self.model.pokedex.listPokemon[pokemon_active_str]
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
                pokemon_withdrawn_str = str(self.enemy_move_data['pokemon_withdrawn'])
                # self.pokemon_withdrawn = self.model.pokedex.listPokemon[pokemon_withdrawn_str]
                new_pokemon_active_str = str(self.enemy_move_data['new_pokemon_active'])
                # self.new_pokemon_active = self.model.pokedex.listPokemon[new_pokemon_active_str]
                index = utils.search_pokemon(self.model.enemy.team, new_pokemon_active_str)
                utils.reset_stats(self.model.enemy.team[0])
                self.model.enemy.swap_position(0, index)
                self.pokemon_enemy_visible = False
                self.pokeball_animations(10, False, False, False, self.model.me.team[0], self.model.enemy.team[0], False, True)
                self.pokeball_animations(10, False, False, True, self.model.me.team[0], self.model.enemy.team[0], False, True)
                self.pokemon_enemy_visible = True
                # todo forse (azzerare special_moves_enemy and count_move_enemy)

    def select_attack(self, move_me):
        prob_accuracy = random.random() * 100
        critic_value = random.uniform(0.85, 1.0)
        self.find_enemy_move(True, move_me, prob_accuracy, critic_value, None, None)
        if self.move_enemy_found and self.enemy_move_data:
            self.read_data()
            game_multiplayer.checks_2_turns_attack(self, move_me, self.move_enemy)

    def game(self):
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
        self.exit_battle = False

        self.explosion_sheet = utils.read_spritesheet_explosion('img/explosion_sheet.png')
        trainer_me = utils.read_spritesheet_trainer_me('img/trainer_sheet.png')
        trainer_enemy = utils.read_spritesheet_trainer_enemy('img/enemy_trainers_sheet.png')
        start_animations = True

        self.pokemon_withdrawn = None
        self.new_pokemon_active = None
        self.move_enemy = None
        self.prob_accuracy = [None, None]
        self.critic_value = [None, None]

        #print('You are player: ', str(self.player))
        self.enemy_lost_connection = False
        self.name_enemy_found = False
        self.team_enemy_found = False
        self.move_enemy_found = False
        self.enemy_use_attack = False
        self.enemy_move_data = None
        self.pokemon_fainted_found = False
        self.pokemon_fainted_data = None

        while self.run:
            self.clock.tick(self.FPS)

            _ = self.keep_connection()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element.most_specific_combined_id == self.btn_change_pokemon.most_specific_combined_id:
                        self.change_pokemon_menu = True
                    if event.ui_element.most_specific_combined_id == self.btn_quit.most_specific_combined_id:
                        self.exit_battle = True
                    if event.ui_element.most_specific_combined_id == self.btn_move1.most_specific_combined_id:
                        if self.model.me.team[0].move1.pp_remain > 0:
                            self.select_attack(self.model.me.team[0].move1)
                        else:
                            self.description_battle = self.model.me.team[0].move1.name +' has 0 pp left.'
                            self.wait(30, False, False)
                    if event.ui_element.most_specific_combined_id == self.btn_move2.most_specific_combined_id:
                        if self.model.me.team[0].move2.pp_remain > 0:
                            self.select_attack(self.model.me.team[0].move2)
                        else:
                            self.description_battle = self.model.me.team[0].move2.name +' has 0 pp left.'
                            self.wait(30, False, False)
                    if event.ui_element.most_specific_combined_id == self.btn_move3.most_specific_combined_id:
                        if self.model.me.team[0].move3.pp_remain > 0:
                            self.select_attack(self.model.me.team[0].move3)
                        else:
                            self.description_battle = self.model.me.team[0].move3.name +' has 0 pp left.'
                            self.wait(30, False, False)
                    if event.ui_element.most_specific_combined_id == self.btn_move4.most_specific_combined_id:
                        if self.model.me.team[0].move4.pp_remain > 0:
                            self.select_attack(self.model.me.team[0].move4)
                        else:
                            self.description_battle = self.model.me.team[0].move4.name +' has 0 pp left.'
                            self.wait(30, False, False)

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
                        self.move_enemy_found = False
                        self.enemy_use_attack = False
                        self.enemy_move_data = None
                        self.move_enemy = None
                        self.prob_accuracy = [None, None]
                        self.critic_value = [None, None]
                        if self.pokemon_changed_not_fainted:
                            self.find_enemy_move(False, None, None, None, self.pokemon_withdrawn, self.new_pokemon_active)
                            if self.move_enemy_found and self.enemy_move_data:
                                self.read_data()
                                game_multiplayer.checks_2_turns_attack(self, None, self.move_enemy)
                        elif self.special_moves_me != None:
                            prob_accuracy = random.random() * 100
                            critic_value = random.uniform(0.85, 1.0)
                            self.find_enemy_move(True, self.special_moves_me, prob_accuracy, critic_value, None, None)
                            if self.move_enemy_found and self.enemy_move_data:
                                self.read_data()
                                game_multiplayer.checks_2_turns_attack(self, self.special_moves_me, self.move_enemy)
                        else:
                            if not self.change_pokemon_menu:
                                if start_animations:
                                    self.start_battle_animations(trainer_me, trainer_enemy, False, False)
                                    self.pokeball_animations(10, False, False, False, self.model.me.team[0], self.model.enemy.team[0], True, True)
                                    self.pokeball_animations(10, False, False, True, self.model.me.team[0], self.model.enemy.team[0], True, True)
                                    start_animations = False
                                    self.pokemon_me_visible = True
                                    self.pokemon_enemy_visible = True
                                else:
                                    self.update_battle_window(True, True)
                                    self.draw_hp(self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
                                self.start_battle = False
                                self.description_battle = 'What will ' + self.model.me.team[0].name + ' do?'
                            else:
                                change_pokemon, self.pokemon_withdrawn, self.new_pokemon_active = self.change_pokemon()
                                if change_pokemon:
                                    self.pokemon_me_visible = False
                                    self.pokeball_animations(10, False, False, False, self.model.me.team[0], self.model.enemy.team[0], True, False)
                                    self.pokeball_animations(10, False, False, True, self.model.me.team[0], self.model.enemy.team[0], True, False)
                                    self.pokemon_me_visible = True
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
                self.start_battle = True
                start_animations = True
                self.description_battle = 'Connection with enemy lost.'
                self.connection_lost_waiting(30)
                self.net = Network()
                self.player = int(self.net.getP())

            self.update_manager_and_display()
        pygame.quit()









