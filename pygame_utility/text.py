import pygame
import pygame.freetype

from pygame_utility.element import Element


class Text(Element):
    def __init__(self, size=(20, 20), position=(0, 0),
                 text='', font=pygame.freetype.SysFont('Arial', 24),
                 fill_color=(0, 0, 0, 0), font_color=(0, 0, 0)):
        super().__init__(size, position)
        self.text = text
        self.image.fill(fill_color)
        self.fill_color = fill_color
        self.font = font
        self.font_color = font_color

    def draw(self, surface):
        self.image.fill(self.fill_color)
        self.font.render_to(self.image, (0, 0), self.text, fgcolor=self.font_color)
        super().draw(surface)
