import pygame
class Button:
    def __init__(self, image, pos, center=True):
        self.imageSurface = image
        self.rect = self.imageSurface.get_rect()
        self.pos = self.rect.center(pos)
        if center:
            self.rect.center = pos
