from Model import Model
import pygame
from pygame.locals import *
import pygame_gui
import button
from random import randrange
import time

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
BG_CHOOSE_POKEMON = ()

class battle_window:
    def __init__(self, model: Model, width, height):
        self.model = model
        self.names = None
        self.i = 0
        self.screen_width = 1300
        self.screen_height = int(1300 * 0.7)

        self.init()

    def init(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Pokemon Battle')
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height), 'themes/button_theming_test_theme.json')
        self.font_name = pygame.font.Font("fonts/VT323-Regular.ttf", 60)
        self.font_hp = pygame.font.Font("fonts/VT323-Regular.ttf", 40)

        #set framerate
        self.clock = pygame.time.Clock()
        self.start_game = False

        self.names = list(self.model.pokedex.listPokemon.keys())
        self.move_up_back = []
        self.move_down_back = []
        self.move_up = []
        self.move_down = []

    def draw_bg(self, draw_bg_img):
        if not draw_bg_img:
            self.battle_bg_img = pygame.image.load('img/battle_bg_1.png').convert_alpha()
            self.battle_bg_img = pygame.transform.scale(self.battle_bg_img, (self.screen_width, self.screen_height * 0.79))
            self.hp_img_me = pygame.image.load('img/life_bar_player.png').convert_alpha()
            self.hp_img_me = pygame.transform.scale(self.hp_img_me, (self.hp_img_me.get_width() / 1.25, self.hp_img_me.get_height() / 1.25))
            self.hp_img_enemy = pygame.image.load('img/life_bar_enemy.png').convert_alpha()
            self.hp_img_enemy = pygame.transform.scale(self.hp_img_enemy, (self.hp_img_enemy.get_width() / 1.25, self.hp_img_enemy.get_height() / 1.25))
        self.screen.blit(self.battle_bg_img, (0, 0))
        self.screen.blit(self.hp_img_me, (self.screen_width * 0.63, self.screen_height * 0.55))
        self.screen.blit(self.hp_img_enemy, (self.screen_width * 0.08, self.screen_height * 0.15))

    def draw_button(self):
        button_width = self.screen_width * 0.18
        button_height = self.screen_height * 0.08
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
        self.btn_move1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.58, self.screen_height * 0.80),
                                                               (button_width, button_height)),
                                     text='move1',
                                     manager=self.manager,
                                     object_id='#btn_move1')

        self.btn_move2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.screen_width * 0.78, self.screen_height * 0.80),
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

    def draw_battle_description(self, text):
        self.battle_description = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render(text, False, (0,0,0))
        self.screen.blit(self.battle_description, (self.screen_width * 0.04, self.screen_height * 0.825))

    def draw_pokemon(self, pokemon_me):
        # pokemon me
        if len(self.move_up_back) == 0:
            self.move_up_back = ['charizard', 'pidgeotto', 'fearow', 'arcanine', 'machamp', 'victreebel', 'dodrio', 'articuno', 'kangaskhan', 'gyarados', 'dragonite', 'rapidash', 'onix']
        if len(self.move_down_back) == 0:
            self.move_down_back = ['bulbasaur', 'ivysaur', 'charmander', 'squirtle', 'caterpie', 'metapod', 'kakuna', 'weedle', 'starly', 'pidgey', 'rattata', 'spearow', 'ekans', 'pikachu',
                                 'sandshrew', 'sandslash', 'nidoran', 'nidorina', 'clefairy', 'vulpix', 'jigglypuff', 'oddish', 'gloom', 'paras', 'venonat',
                                 'diglett', 'dugtrio', 'meowth', 'psyduck', 'mankey', 'growlithe', 'poliwag', 'poliwhirl', 'abra', 'bellsprout', 'geodude', 'graveler', 'slowpoke', 'magnemite',
                                 'seel', 'grimer', 'shellder', 'krabby', 'voltorb', 'exeggcute', 'cubone', 'marowak', 'chansey', 'tangela', 'horsea', 'seadra', 'goldeen', 'seaking',
                                 'staryu', 'ditto', 'jolteon', 'omanyte', 'porygon', 'kabuto']

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
        self.btn_move1.set_text(str(pokemon_me.move1.name))
        self.btn_move2.set_text(str(pokemon_me.move2.name))
        self.btn_move3.set_text(str(pokemon_me.move3.name))
        self.btn_move4.set_text(str(pokemon_me.move4.name))

        # pokemon enemy
        if len(self.move_up) == 0:
            self.move_up = ['charizard', 'pidgeot', 'arcanine', 'machoke', 'machamp', 'rapidash', 'onix', 'exeggutor', 'kangaskhan', 'lapras', 'articuno', 'mewtwo', 'nidoqueen', 'nidoking',
                            'wartortle', 'venusaur', 'ninetales', 'fearow', 'pidgeotto', 'persian', 'alakazam', 'slowbro', 'dodrio', 'dewgong', 'hitmonlee', 'rhydon', 'snorlax', 'dragonite',
                            'moltres', 'victreebel']
        if len(self.move_down) == 0:
            self.move_down = ['rattata', 'bulbasaur', 'sandshrew', 'paras', 'diglett', 'ditto', 'omanyte', 'porygon', 'nidoran', 'spearow', 'jigglypuff', 'paras', 'growlithe', 'abra', 'grimer',
                              'krabby', 'exeggcute', 'cubone', 'kabuto']
        pokemon_enemy = self.names[self.i]
        pokemon_enemy_image = pygame.image.load('img_pokemon_battle_png/' + pokemon_enemy.lower() + '.png').convert_alpha()
        pokemon_enemy_image = pygame.transform.scale(pokemon_enemy_image, (pokemon_enemy_image.get_width() * 3, pokemon_enemy_image.get_height() * 3))
        if pokemon_enemy.lower() in self.move_up:
            self.screen.blit(pokemon_enemy_image, (self.screen_width * 0.73, self.screen_height * 0.015))
        elif pokemon_enemy.lower() in self.move_down:
            self.screen.blit(pokemon_enemy_image, (self.screen_width * 0.73, self.screen_height * 0.065))
        else:
            self.screen.blit(pokemon_enemy_image, (self.screen_width * 0.73, self.screen_height * 0.045))
        draw_name_enemy = self.font_name.render(pokemon_enemy, False, (0,0,0))
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

    def draw_pokemon_choose_menu(self):
        # self.i = randrange(len(self.names))
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
        #self.i += 1

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

    def game(self):
        FPS = 60
        run = True
        start_img = pygame.image.load('img/start_btn.png').convert_alpha()
        exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()

        start_button = button.Button(self.screen_width // 2 - 130, self.screen_height // 2 - 150, start_img, 1)
        exit_button = button.Button(self.screen_width // 2 - 110, self.screen_height // 2 + 50, exit_img, 1)
        draw_bg_img = False
        draw_Button_battle = False
        change_pokemon_menu = False

        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element.most_specific_combined_id == self.btn_change_pokemon.most_specific_combined_id:
                        change_pokemon_menu = True
                    if event.ui_element.most_specific_combined_id == self.btn_quit.most_specific_combined_id:
                        self.i -= 1
                        self.draw_battle_description(self.names[self.i] + ' it\'s your turn')
                    if event.ui_element.most_specific_combined_id == self.btn_move1.most_specific_combined_id:
                        self.i += 10
                        self.draw_battle_description(self.names[self.i] + ' it\'s your turn')

                self.manager.process_events(event)

            if not self.start_game:
                #draw menu
                self.screen.fill(BG)
                #add buttons
                if start_button.draw(self.screen):
                    self.start_game = True
                    # start_intro = True
                if exit_button.draw(self.screen):
                    run = False
            else:
                if not change_pokemon_menu:
                    self.screen.fill(BG)
                    self.draw_bg(draw_bg_img)
                    self.draw_battle_description(str(self.model.me.team[0].name) + ' it\'s your turn')
                    if not draw_Button_battle:
                        self.draw_button()
                        self.draw_button_moves()
                        draw_Button_battle = True
                    self.draw_pokemon(self.model.me.team[0])

                    hp_me = self.model.me.team[0].battleHP_actual
                    max_hp_me = self.model.me.team[0].battleHP
                    self.renderHPBar(self.hp_img_enemy.get_width() * 0.62, self.hp_img_enemy.get_height() * 0.275, (self.screen_width * 0.178, self.screen_height * 0.16), max_hp_me, hp_me) # HP enemy
                    self.renderHPBar(self.hp_img_me.get_width() * 0.6, self.hp_img_me.get_height() * 0.18, (self.screen_width * 0.732, self.screen_height * 0.552), max_hp_me, hp_me) # HP me
                    draw_hp_number = self.font_hp.render(str(hp_me) + ' / ' + str(max_hp_me), False, (0,0,0))
                    self.screen.blit(draw_hp_number, (self.screen_width * 0.75, self.screen_height * 0.62))
                else:
                    self.screen.fill(BG)
                    draw_Button_battle = False
                    self.btn_change_pokemon.hide()
                    self.btn_quit.hide()
                    self.btn_move1.hide()
                    self.btn_move2.hide()
                    self.btn_move3.hide()
                    self.btn_move4.hide()
                    self.draw_pokemon_choose_menu()
                    self.draw_HP_pokemon_choose_menu()

                    x, y = pygame.mouse.get_pos()
                    print(x , y)
                    for event in pygame.event.get():
                        if self.rect_pokemon_list_menu_active.collidepoint(pygame.mouse.get_pos()):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                change_pokemon_menu = False
                        if self.rect_pokemon_list_menu_deactive1.collidepoint(pygame.mouse.get_pos()):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                change_pokemon_menu = False
                        if self.rect_pokemon_list_menu_deactive2.collidepoint(pygame.mouse.get_pos()):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                change_pokemon_menu = False
                        if self.rect_pokemon_list_menu_deactive3.collidepoint(pygame.mouse.get_pos()):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                change_pokemon_menu = False
                        if self.rect_pokemon_list_menu_deactive4.collidepoint(pygame.mouse.get_pos()):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                change_pokemon_menu = False
                        if self.rect_pokemon_list_menu_deactive5.collidepoint(pygame.mouse.get_pos()):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                change_pokemon_menu = False
                        if self.rect_text_exit.collidepoint(pygame.mouse.get_pos()):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                change_pokemon_menu = False


            time_delta = self.clock.tick(FPS)/1000.0
            self.manager.update(time_delta)

            self.manager.draw_ui(self.screen)
            pygame.display.update()
        pygame.quit()









