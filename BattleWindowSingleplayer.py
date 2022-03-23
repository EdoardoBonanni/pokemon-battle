from models.Model import Model
import pygame
import pygame_gui
from utility import utils, game_singleplayer, show_screen_elements
import os


class BattleWindowSingleplayer:
    """
    PyGame window for single-player mode.
    """
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
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height), 'themes/button_theming_test_theme.json')  # PyGame gui manager.
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
            self.name_enemy = pygame.font.Font("fonts/VT323-Regular.ttf", 30).render("Enemy: CPU", False, (0, 0, 0))
            self.draw_bg_img = True
        self.screen.blit(self.battle_bg_img, (0, 0))
        self.screen.blit(self.hp_img_me, (self.screen_width * 0.63, self.screen_height * 0.55))
        self.screen.blit(self.hp_img_enemy, (self.screen_width * 0.08, self.screen_height * 0.15))
        self.screen.blit(self.name_player, (self.screen_width * 0.64, self.screen_height * 0.72))
        self.screen.blit(self.name_enemy, (self.screen_width * 0.112, self.screen_height * 0.03))


    def draw_button(self):
        """
        Draw 'Change Pokemon' and 'Quit' buttons on the screen.
        :return:
        """
        button_width = self.screen_width * 0.18
        button_height = self.screen_height * 0.08
        self.btn_change_pokemon = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width * 0.05, self.screen_height * 0.90),
                                      (button_width, button_height)),
            text='Change Pokemon',
            manager=self.manager,
            object_id='#btn_change_pokemon')

        self.btn_quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width * 0.25, self.screen_height * 0.90),
                                      (button_width, button_height)),
            text='Quit',
            manager=self.manager,
            object_id='#btn_quit')


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
            self.draw_button()
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

    def select_pokemon_from_menu_singleplayer(self, event, rect_menu, pokemon_index, pokemon_active, pokemon_changed):
        """
        Select a Pokemon from team in the choice menu.
        :param event: PyGame event.
        :param rect_menu: PyGame rect.
        :param pokemon_index: Pokemon index in the team.
        :param pokemon_active: Pokemon active in battle.
        :param pokemon_changed: check if Pokemon is changed or not.
        :return: pokemon_changed.
        """
        if rect_menu.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if self.model.me.team[pokemon_index].battleHP_actual > 0:
                    if pokemon_active.battleHP_actual != 0:
                        self.pokemon_changed_not_fainted = True
                    utils.reset_stats(pokemon_active)
                    self.special_moves_me = None
                    self.count_move_me = 0
                    self.model.me.swap_position(0, pokemon_index)
                    self.change_pokemon_menu = False
                    pokemon_changed = True
        return pokemon_changed

    def change_pokemon(self):
        """
        Change Pokemon on screen and show the other one that is chosen.
        :return: Pokemon changed.
        """
        self.screen.fill(self.bg_color)
        show_screen_elements.hide_buttons(self)
        show_screen_elements.draw_team_choice_menu(self)
        show_screen_elements.draw_HP_pokemon_choice_menu(self)
        pokemon_changed = False

        for event in pygame.event.get():
            if self.rect_pokemon_list_menu_active.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[0].battleHP_actual > 0:
                        self.change_pokemon_menu = False

            pokemon_changed = self.select_pokemon_from_menu_singleplayer(event, self.rect_pokemon_list_menu_deactive1, 1, self.model.me.team[0], pokemon_changed)
            pokemon_changed = self.select_pokemon_from_menu_singleplayer(event, self.rect_pokemon_list_menu_deactive2, 2, self.model.me.team[0], pokemon_changed)
            pokemon_changed = self.select_pokemon_from_menu_singleplayer(event, self.rect_pokemon_list_menu_deactive3, 3, self.model.me.team[0], pokemon_changed)
            pokemon_changed = self.select_pokemon_from_menu_singleplayer(event, self.rect_pokemon_list_menu_deactive4, 4, self.model.me.team[0], pokemon_changed)
            pokemon_changed = self.select_pokemon_from_menu_singleplayer(event, self.rect_pokemon_list_menu_deactive5, 5, self.model.me.team[0], pokemon_changed)

            if self.rect_text_exit.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self.model.me.team[0].battleHP_actual > 0:
                        self.change_pokemon_menu = False
        self.description_battle = 'What will ' + self.model.me.team[0].name + ' do?'
        return pokemon_changed

    def battle_events_singleplayer(self, event, button_move, move_id):
        """
        Check the move choice and after that all animation start.
        :param event: PyGame event.
        :param button_move: one of the four button move.
        :param move_id: one of the four Pokemon move.
        :return:
        """
        if event.ui_element.most_specific_combined_id == button_move.most_specific_combined_id:
            if move_id.pp_remain > 0:
                move_enemy = utils.choose_enemy_move(self)
                game_singleplayer.checks_2_turns_attack(self, move_id, move_enemy)
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
        self.exit_battle = False

        self.explosion_sheet = utils.read_spritesheet_explosion('img/explosion_sheet.png')
        trainer_me = utils.read_spritesheet_trainer_me('img/trainer_sheet.png')
        trainer_enemy = utils.read_spritesheet_trainer_enemy('img/enemy_trainers_sheet.png')
        start_animations = True

        # while to run the Game.
        while self.run:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_battle = True
                    self.run = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element.most_specific_combined_id == self.btn_change_pokemon.most_specific_combined_id:
                        self.change_pokemon_menu = True
                    if event.ui_element.most_specific_combined_id == self.btn_quit.most_specific_combined_id:
                        self.exit_battle = True
                    self.battle_events_singleplayer(event, self.btn_move1, self.model.me.team[0].move1)
                    self.battle_events_singleplayer(event, self.btn_move2, self.model.me.team[0].move2)
                    self.battle_events_singleplayer(event, self.btn_move3, self.model.me.team[0].move3)
                    self.battle_events_singleplayer(event, self.btn_move4, self.model.me.team[0].move4)

                self.manager.process_events(event)

            # exit from Game and return to GameModeSelection.
            if self.exit_battle:
                show_screen_elements.exit_battle_operations(self)
                pygame.quit()
                return None

            # check if Pokemon in battle is changed and not fainted, if so the enemy has to attack.
            if self.pokemon_changed_not_fainted:
                move_enemy = utils.choose_enemy_move(self)
                game_singleplayer.check_turn_type(self, None, move_enemy)
            # check if Pokemon of player me do a special move.
            elif self.special_moves_me is not None:
                move_enemy = utils.choose_enemy_move(self)
                game_singleplayer.checks_2_turns_attack(self, self.special_moves_me, move_enemy)
            else:
                if not self.change_pokemon_menu:
                    # check if the Game is started and if so run the first animations.
                    if start_animations:
                        show_screen_elements.start_battle_animations(self, trainer_me, trainer_enemy, False, False)
                        show_screen_elements.pokeball_animations(self, 10, False, False, False, self.model.me.team[0],
                                                 self.model.enemy.team[0], True, True)
                        show_screen_elements.pokeball_animations(self, 10, False, False, True, self.model.me.team[0],
                                                 self.model.enemy.team[0], True, True)
                        start_animations = False
                        self.pokemon_me_visible = True
                        self.pokemon_enemy_visible = True
                    # normal execution of the Game.
                    else:
                        self.update_battle_window(True, True)
                        show_screen_elements.draw_hp(self, self.model.me.team[0].battleHP_actual, self.model.enemy.team[0].battleHP_actual)
                    self.start_battle = False
                    self.description_battle = 'What will ' + self.model.me.team[0].name + ' do?'
                # check if the change Pokemon menu is active.
                else:
                    change_pokemon = self.change_pokemon()
                    # Check if user change Pokemon and if so the animation start.
                    if change_pokemon:
                        self.pokemon_me_visible = False
                        show_screen_elements.pokeball_animations(self, 10, False, False, False, self.model.me.team[0],
                                                 self.model.enemy.team[0], True, False)
                        show_screen_elements.pokeball_animations(self, 10, False, False, True, self.model.me.team[0],
                                                 self.model.enemy.team[0], True, False)
                        self.pokemon_me_visible = True

            show_screen_elements.update_manager_and_display(self)
        pygame.quit()
