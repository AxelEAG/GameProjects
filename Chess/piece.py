import pygame

from pygame.sprite import Sprite


class Piece(Sprite):

    def __init__(self, piece_type, rows, piece_number, positions):
        super().__init__()
        if rows == 1:
            self.side = ''
            self.direction = -1
        else:
            self.side = 'E'
            self.direction = 1
        self.image = pygame.image.load('images/' + self.side + positions[piece_type][0] + '.png')
        self.rect = self.image.get_rect()
        self.type = self.side + positions[piece_type][0]
        self.rect.x = self.rect.width * (positions[piece_type][5] + piece_number * positions[piece_type][2])
        self.rect.y = self.rect.height * (positions[piece_type][3] + rows * positions[piece_type][4])
        if 'Pawn' in self.type:
            self.enpassant = False
        if 'King' in self.type:
            self.castling = True
