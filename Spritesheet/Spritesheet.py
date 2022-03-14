import pygame
import json


class Spritesheet:
    """
    Class that allows reading sprite-sheets.
    """
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = self.filename.replace('img', 'Spritesheet')
        self.meta_data = self.meta_data.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        """
        Create the sprite-sheet on a PyGame surface.
        :param x: coordinate x.
        :param y: coordinate y.
        :param w: width surface.
        :param h: height surface.
        :return: the PyGame surface.
        """
        sprite = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        """
        Get information from sprite-sheet data.
        :param name: Frame name.
        :return: the PyGame surface.
        """
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h).convert_alpha()
        return image
