from Model import Model
import pygame
from pygame.locals import *
import pygame_gui
import button
from battle_window import battle_window

#define colours
BG_GREEN = (144, 201, 120)
BG = (224, 235, 235)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

class start_battle_window:
    def __init__(self, model: Model, width, height):
        self.model = model
        self.screen_width = 1300
        self.screen_height = int(1300 * 0.7)

        self.init()

    def init(self):
        pygame.init()

        # icon = pygame.image.load('img/pokemon.png').convert_alpha()
        # pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Pokemon Battle')

        #set framerate
        self.clock = pygame.time.Clock()

    def game(self):
        FPS = 60
        run = True
        self.start_battle = False
        start_img = pygame.image.load('img/start_btn.png').convert_alpha()
        exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()

        start_button = button.Button(self.screen_width // 2 - 130, self.screen_height // 2 - 150, start_img, 1)
        exit_button = button.Button(self.screen_width // 2 - 110, self.screen_height // 2 + 50, exit_img, 1)

        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #draw menu
            self.screen.fill(BG)
            #add buttons
            if start_button.draw(self.screen):
                self.start_battle = True
                #run = False

            if exit_button.draw(self.screen):
                pygame.quit()
                return None

            if self.start_battle:
                self.start_game()

            pygame.display.update()

        # if start_battle:
        #     self.start_game()
        # else:
        #     pygame.quit()

    def start_game(self):
        battle_window_obj = battle_window(self.model, self.screen_width, self.screen_height)
        battle_window_obj.game()
        self.start_battle = False
        del battle_window_obj
