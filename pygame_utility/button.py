import pygame

from pygame_utility.element import Element


class Button(Element):
    def __init__(self, size=(20, 20), position=(0, 0), fill_color=(255, 255, 255), click_color=(0, 0, 0)):
        super().__init__(size, position)
        self.state = False
        self.fill_color = fill_color
        self.click_color = click_color
        self.image.fill(fill_color)

    def event_update(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.on_click()

    def on_click(self):
        pass

    def draw(self, surface):
        if pygame.mouse.get_pressed(3)[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill(self.click_color)
        else:
            self.image.fill(self.fill_color)
        super().draw(surface)
