import pygame

pygame.init()

class Element(pygame.sprite.Sprite):
    def __init__(self, size=(0, 0), position=(0, 0)):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.enabled = True

    def event_update(self, event):
        pass

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

