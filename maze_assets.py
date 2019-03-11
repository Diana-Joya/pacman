import pygame
from pygame.sprite import Sprite


class MakeAsset(Sprite):
    def __init__(self, settings, screen, filename):
        super(MakeAsset, self).__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load("images/" + filename + ".png")
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        self.width = self.rect.width

    def blitme(self):
        self.screen.blit(self.image, self.rect)
