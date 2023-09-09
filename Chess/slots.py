import pygame
from pygame.sprite import Sprite



class Slots(Sprite):

    def __init__(self, x_pos, y_pos):
        super().__init__()

        self.image = pygame.image.load('images/Available_Slots.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.enemy = ''
        self.castling = False