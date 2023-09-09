import sys
import pygame

from piece import Piece
from slots import Slots


class ChessGame:

    def __init__(self):
        self._create_window()
        self.pieces = pygame.sprite.Group()
        self.slots = pygame.sprite.Group()
        self._create_pieces()
        self.turn = -1
        self.echeck = False
        self.check = False

    def run_game(self):
        while True:
            self._check_events()
            pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._move_pieces()

    def _move_pieces(self):
        coordinates = pygame.mouse.get_pos()
        for piece in self.pieces:
            if piece.direction == self.turn:
                if self._detect_piece(piece, coordinates):
                    break
        else:

            self._detect_slot(coordinates)
            self._move_piece()
            self._clear_slots()
            self._close_enpassant()

    def _move_piece(self):
        if self.clicked_slot:
            if 'Pawn' in self.clicked_piece.type:
                if self.clicked_slot.rect.y == self.clicked_piece.rect.y + 2 * self.clicked_piece.direction * self.clicked_piece.rect.height:
                    self.clicked_piece.enpassant = True
            if 'King' in self.clicked_piece.type:
                self.clicked_piece.castling = False
            self._clean_slot()
            self._enpassant_kill()
            self.clicked_piece.rect.x = self.clicked_slot.rect.x
            self.clicked_piece.rect.y = self.clicked_slot.rect.y
            self.turn *= -1
            self._in_check()
            self._show_options(self.clicked_piece)
            if self.clicked_slot.castling:
                self.clicked_slot.castling = False
                for piece in self.pieces:
                    if piece.rect.collidepoint(self.clicked_piece.rect.x + 100, self.clicked_piece.rect.y):
                        slot = Slots(self.clicked_piece.rect.x + 100, self.clicked_piece.rect.y)
                        slot.image = pygame.image.load('images/White.png')
                        self.slots.add(slot)
                        self.slots.draw(self.screen)
                        slot.kill()
                        piece.rect.x = self.clicked_piece.rect.x - 100

    def _in_check(self):
        for piece in self.pieces:
            self._show_options(piece)
            self._clear_slots()

    def _detect_piece(self, piece, coordinates):
        if piece.rect.collidepoint(coordinates):
            self.clicked_piece = piece
            self._clear_slots()
            self._show_options(self.clicked_piece)
            return True

    def _clear_slots(self):
        for slot in self.slots.copy():
            if (slot.rect.x + slot.rect.y) % 200 == 0:
                slot.image = pygame.image.load('images/White.png')
            else:
                slot.image = pygame.image.load('images/Black.png')
            self.slots.draw(self.screen)
            slot.kill()
        self.pieces.draw(self.screen)

    def _show_options(self, piece):
        if 'Pawn' in piece.type:
            self._pawn_options(piece)
        elif 'Bishop' in piece.type:
            self._bishop_options(piece)
        elif 'Knight' in piece.type:
            self._knight_options(piece)
        elif 'Rook' in piece.type:
            self._rook_options(piece)
        elif 'Queen' in piece.type:
            self._queen_options(piece)
        elif 'King' in piece.type:
            self._king_options(piece)
        self.slots.draw(self.screen)

    def _clean_slot(self):
        slot = Slots(self.clicked_piece.rect.x, self.clicked_piece.rect.y)
        self.slots.add(slot)
        self.slots.draw(self.screen)

    def _detect_slot(self, coordinates):
        self.clicked_slot = False
        for slot in self.slots:
            if slot.rect.collidepoint(coordinates):
                self.clicked_slot = slot
                break
            else:
                self.clicked_slot = False

    def _create_pieces(self):
        positions = {0: ('Rook', 2, 7, 0, 7, 0), 1: ('Knight', 2, 5, 0, 7, 1), 2: ('Bishop', 2, 3, 0, 7, 2),
                     3: ('Queen', 1, 0, 0, 7, 3), 4: ('King', 1, 0, 0, 7, 4), 5: ('Pawn', 8, 1, 1, 5, 0)}
        # Format: Piece, amount, space between them, row, enemy separation, x_position.
        for piece_type in range(6):
            for rows in range(2):
                for piece_number in range(positions[piece_type][1]):
                    piece = Piece(piece_type, rows, piece_number, positions)
                    self.pieces.add(piece)
        self.pieces.draw(self.screen)

    def _pawn_options(self, piece):
        for rows in range(1, 3):
            slot = Slots(piece.rect.x, piece.rect.y + piece.direction * rows * piece.rect.height)
            if self._blocked_pawn(slot):
                break
            self.slots.add(slot)
            if piece.direction == -1:
                if piece.rect.y != 7 * piece.rect.height - piece.rect.height:
                    break
            elif piece.rect.y != piece.rect.height:
                break

        for dirs in [-1, 1]:
            slot = Slots(piece.rect.x + dirs * piece.rect.width, piece.rect.y + piece.direction * piece.rect.height)
            self._can_eat(slot, piece)

        self._en_passant(piece)

    def _bishop_options(self, piece):

        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        diagonals = []
        collision = False
        while x1 >= 100 and y1 >= 100:
            x1 -= 100
            y1 -= 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        diagonals.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            diagonals.append((x1, y1))

        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        collision = False
        while x1 >= 100 and y1 <= 700:
            x1 -= 100
            y1 += 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        diagonals.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            diagonals.append((x1, y1))

        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        collision = False
        while x1 <= 700 and y1 <= 700:
            x1 += 100
            y1 += 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        diagonals.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            diagonals.append((x1, y1))

        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        collision = False
        while x1 <= 700 and y1 >= 100:
            x1 += 100
            y1 -= 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        diagonals.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            diagonals.append((x1, y1))

        for cords in diagonals:
            slot = Slots(cords[0], cords[1])
            self._can_eat(slot, piece)
            self.slots.add(slot)
        self.slots.draw(self.screen)

    def _knight_options(self, piece):
        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        for cord in [(x1 + 200, y1 + 100), (x1 + 200, y1 - 100), (x1 - 200, y1 + 100), (x1 - 200, y1 - 100),
                     (x1 + 100, y1 + 200), (x1 - 100, y1 + 200), (x1 + 100, y1 - 200), (x1 - 100, y1 - 200)]:
            if cord[0] < 0 or cord[0] > 700 or cord[1] < 0 or cord[1] > 700:
                continue
            else:
                collision = False
                for pice in self.pieces:
                    if pice.rect.collidepoint((cord[0], cord[1])):
                        if pice.direction == self.turn:
                            collision = True
                        break
                if collision:
                    continue
                else:
                    slot = Slots(cord[0], cord[1])
                    self._can_eat(slot, piece)
                    self.slots.add(slot)

    def _rook_options(self, piece):
        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        lines = []
        collision = False
        while x1 >= 100:
            x1 -= 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        lines.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            lines.append((x1, y1))

        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        collision = False
        while x1 <= 700:
            x1 += 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        lines.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            lines.append((x1, y1))

        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        collision = False
        while y1 >= 100:
            y1 -= 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        lines.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            lines.append((x1, y1))

        x1 = int(piece.rect.x)
        y1 = int(piece.rect.y)
        collision = False
        while y1 <= 700:
            y1 += 100
            for pice in self.pieces:
                if pice.rect.collidepoint((x1, y1)):
                    if pice.direction != self.turn:
                        lines.append((x1, y1))
                    collision = True
                    break
            if collision:
                break
            lines.append((x1, y1))

        for cords in lines:
            slot = Slots(cords[0], cords[1])
            self._can_eat(slot, piece)
            self.slots.add(slot)
        self.slots.draw(self.screen)

    def _queen_options(self, piece):
        self._bishop_options(piece)
        self._rook_options(piece)

    def _king_options(self, piece):
        self._castling(piece)
        for x_pos in [piece.rect.x - 100, piece.rect.x, piece.rect.x + 100]:
            for y_pos in [piece.rect.y - 100, piece.rect.y, piece.rect.y + 100]:
                collision = False
                for pice in self.pieces:
                    if pice.rect.collidepoint((x_pos, y_pos)):
                        if pice.direction == self.turn:
                            collision = True
                        break
                if collision:
                    continue
                slot = Slots(x_pos, y_pos)
                self._can_eat(slot, piece)
                self.slots.add(slot)
        self.slots.draw(self.screen)

    def _en_passant(self, piece):
        for pieces in self.pieces:
            if 'Pawn' in pieces.type:
                if pieces.side != piece.side:
                    for dirs in [-1, 1]:
                        if pieces.rect.x == piece.rect.x + dirs * piece.rect.width and pieces.rect.y == piece.rect.y:
                            if piece.side == '':
                                line = 3
                            else:
                                line = 4
                            if piece.rect.y == line * piece.rect.height:
                                if pieces.enpassant:
                                    slot = Slots(piece.rect.x + dirs * piece.rect.width,
                                                 piece.rect.y + piece.direction * piece.rect.height)
                                    slot.enemy = pieces
                                    self.slots.add(slot)

    def _close_enpassant(self):
        for piece in self.pieces:
            if 'Pawn' in piece.type:
                if piece.direction == self.turn:
                    piece.enpassant = False

    def _enpassant_kill(self):
        if self.clicked_slot.enemy:
            if (self.clicked_slot.enemy.rect.x + self.clicked_slot.enemy.rect.y) % 200 == 0:
                self.clicked_slot.enemy.image = pygame.image.load('images/White.png')
            else:
                self.clicked_slot.enemy.image = pygame.image.load('images/Black.png')
            self.pieces.draw(self.screen)
            self.clicked_slot.enemy.kill()

    def _blocked_pawn(self, slot):
        for pieces in self.pieces:
            if slot.rect.colliderect(pieces):
                slot.kill()
                return True

    def _can_eat(self, slot, piece):
        for pieces in self.pieces:
            if slot.rect.colliderect(pieces):
                if pieces.side != piece.side:
                    slot.enemy = pieces
                    if 'King' in pieces.type:
                        self.check = True
                    self.slots.add(slot)
                    break
        else:
            slot.kill()

    def _castling(self, king):
        if king.castling:
            for piece in self.pieces:
                if piece.rect.collidepoint(king.rect.x + 100, king.rect.y) or piece.rect.collidepoint(king.rect.x + 200, king.rect.y):
                    break
            else:
                slot = Slots(king.rect.x + 200, king.rect.y)
                slot.castling = True
                self.slots.add(slot)

    def _create_window(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.image = pygame.image.load('images/Board.bmp')
        self.screen.blit(self.image, (0, 0))
        pygame.display.update()

if '__main__' == __name__:
    game = ChessGame()
    game.run_game()
