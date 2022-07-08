import pygame

from pygame_utility.element import Element


class Group(Element):
    def __init__(self, size=(0, 0), position=(0, 0),  elements=None):
        super().__init__(size, position)
        if elements is None:
            elements = {}
        self.elements = elements
        self.image.fill((0, 0, 0, 0))

    def event_update(self, event):
        for name, element in self.elements.items():
            element.event_update(event)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        for name, element in self.elements.items():
            element.draw(surface)

    def add_element(self, index, element):
        self.elements[index] = element
        element.rect.x = element.rect.x + self.rect.x
        element.rect.y = element.rect.y + self.rect.y
