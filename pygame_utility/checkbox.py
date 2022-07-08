import pygame

from pygame_utility.element import Element


class Checkbox(Element):
    def __init__(self, size=(20, 20), position=(0, 0), fill_color=(255, 255, 255), check_color=(0, 0, 0)):
        super().__init__(size, position)

        self.state = False

        self.fill_color = fill_color
        self.check_color = check_color
        self.image.fill(fill_color)

    def event_update(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.toggle()

    def toggle(self):
        self.state = not self.state

    def draw(self, surface):
        if self.state:
            self.image.fill(self.check_color)
        else:
            self.image.fill(self.fill_color)
        super().draw(surface)
