import pygame
import random
import sys


class Snake:
    def __init__(self, length=3, speed=200):
        self.length = length
        self.direction = [0, 0]
        self.location = []
        self.speed = speed # miliseconds to update
        self.growth = 1
        self.alive = True
        self.can_change = True


class Apple:
    def __init__(self, amount=1):
        self.amount = amount
        self.locations = []


class Board:
    def __init__(self, width, height, pixel_dim):
        self.width = width
        self.height = height
        self.pixel_dim = pixel_dim  # same amount length and height
        self.pixel_w = self.width/self.pixel_dim
        self.pixel_h = self.height/self.pixel_dim


class Game:
    def __init__(self, width=600, height=600, pixel_dim=30, length=3, speed=200, amount=1):
        self.board = Board(width, height, pixel_dim)
        self.snake = Snake(length, speed)
        self.apple = Apple(amount)
        self.screen = pygame.display.set_mode((self.board.width, self.board.height))
        pygame.display.set_caption("The Snake Game")

        self.snake_move = pygame.USEREVENT + 1
        pygame.time.set_timer(self.snake_move, self.snake.speed)

        self.generate_snake()

        for i in range(self.apple.amount):
            self.generate_apple()

    def run_game(self):
        while self.snake.alive:
            self.manage_events()
            self.render()

            pygame.display.flip()
        menu1 = Menu()

    def render(self):
        self.render_board()
        self.render_snake()
        self.render_apples()
        self.render_grid()

    def render_board(self):
        for i in range(self.board.pixel_dim):
            for j in range(self.board.pixel_dim):
                pygame.draw.rect(self.screen, (150, 150, 150), (i * self.board.pixel_w, j * self.board.pixel_h,
                                                                self.board.pixel_w, self.board.pixel_h))

    def render_snake(self):

        for i in range(self.snake.length):
            x, y = self.snake.location[i]
            pygame.draw.rect(self.screen, (0, 150, 0), (x * self.board.pixel_w, y * self.board.pixel_h,
                                                        self.board.pixel_w, self.board.pixel_h))

    def render_apples(self):
        for i in range(self.apple.amount):
            x, y = self.apple.locations[i]
            pygame.draw.rect(self.screen, (150, 0, 0), (x * self.board.pixel_w, y * self.board.pixel_h,
                                                        self.board.pixel_w, self.board.pixel_h))

    def render_grid(self):
        for i in range(self.board.pixel_dim):
            for j in range(self.board.pixel_dim):
                pygame.draw.rect(self.screen, (0, 0, 0), (i * self.board.pixel_w, j * self.board.pixel_h,
                                                          self.board.pixel_w, self.board.pixel_h), width=1)

    def manage_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == self.snake_move:
                self.move_snake()
                self.snake.can_change = True

            if event.type == pygame.KEYDOWN:
                if self.snake.can_change:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if self.snake.direction != [0, 1]:
                            self.snake.direction = [0, -1]
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if self.snake.direction != [0, -1]:
                            self.snake.direction = [0, 1]
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if self.snake.direction != [1, 0]:
                            self.snake.direction = [-1, 0]
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if self.snake.direction != [-1, 0]:
                            self.snake.direction = [1, 0]
                    self.snake.can_change = False

    def generate_apple(self):
        available = []
        for i in range(self.board.pixel_dim):
            for j in range(self.board.pixel_dim):
                if [i, j] not in self.snake.location:
                    available.append([i, j])
        x, y = random.choice(available)
        self.apple.locations.append([x, y])

    def generate_snake(self):
        x = random.randint(0, self.board.pixel_dim - 1)
        y = random.randint(2, self.board.pixel_dim - self.snake.length - 1)
        self.snake.location.append([x, y])

        for i in range(self.snake.length - 1):
            x, y = self.snake.location[-1]
            self.snake.location.append([x, y + 1])

    def move_snake(self):
        if self.snake.direction != [0, 0]:
            head_pos = [self.snake.location[0][0] + self.snake.direction[0],
                        self.snake.location[0][1] + self.snake.direction[1]]

            self.snake.location.insert(0, head_pos)
            if not self.grow_snake():
                del self.snake.location[-1]

            if self.snake_died(self.snake.location):
                self.snake.alive = False

            self.grow_snake()

    def grow_snake(self):
        for i in range(self.apple.amount):
            if self.snake.location[0] == self.apple.locations[i]:
                self.snake.length += self.snake.growth
                del self.apple.locations[i]
                self.generate_apple()
                return True
        return False

    def snake_died(self, positions):
        head = positions[0]
        if head in self.snake.location[1:]:
            return True
        if head[0] < 0 or head[0] >= self.board.pixel_dim:
            return True
        if head[1] < 0 or head[1] >= self.board.pixel_dim:
            return True
        return False


# {1: "Start", 2: "Difficulty", 3: "Minigames"}

class Menu:
    pygame.init()
    menu_types = {"MainMenu": {1: "Start", 2: "Difficulty", 3: "Minigames"},
                  "Difficulty": {1: "Easy", 2: "Medium", 3: "Hard", 4: "Impossible"},
                  "MiniGames": {1: "More Apples", 2: "etc."}}

    def __init__(self, width=600, height=600, menu_type="Menu"):

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Snake Game")
        self.active = True
        self.type = menu_type
        self.texts = self.menu_types[self.type]
        mouse = pygame.mouse.get_pos()
        self.x, self.y = mouse

        self.game_loop()

    def game_loop(self):
        while self.active:
            mouse = pygame.mouse.get_pos()
            self.x, self.y = mouse
            self.create_buttons()
            self.manage_events()
            pygame.display.flip()

    def manage_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.manage_buttons()

    def manage_buttons(self):
        height = self.height / (2 * len(self.texts))
        x_center = self.width / 2
        width = 0.4 * self.width
        height2 = 0.95 * height

        if self.type == "MainMenu":
            def start():
                game = Game(600, 600, 15, 3, 300, 1)
                self.active = False
                game.run_game()

            def difficulty():
                self.active = False
                menu = Menu(menu_type="Difficulty")

            def minigames():
                self.active = False
                menu = Menu(menu_type="MiniGames")

            functions = {0: start, 1: difficulty, 2: minigames}
        elif self.type == "Difficulty":
            def easy():
                game = Game(600, 600, 15, 3, 300, 2)
                self.active = False
                game.run_game()

            def medium():
                game = Game(600, 600, 15, 3, 200, 1)
                self.active = False
                game.run_game()

            def hard():
                game = Game(600, 600, 15, 3, 100, 1)
                self.active = False
                game.run_game()

            def impossible():
                game = Game(600, 600, 15, 3, 50, 1)
                self.active = False
                game.run_game()

            functions = {0: easy, 1: medium, 2: hard, 3: impossible}
        elif self.type == "MiniGames":
            def easy():
                game = Game(600, 600, 15, 3, 300, 2)
                self.active = False
                game.run_game()

            def medium():
                game = Game(600, 600, 15, 3, 200, 1)
                self.active = False
                game.run_game()

            def hard():
                game = Game(600, 600, 15, 3, 100, 1)
                self.active = False
                game.run_game()

            def impossible():
                game = Game(600, 600, 15, 3, 50, 1)
                self.active = False
                game.run_game()

            functions = {0: easy, 1: medium, 2: hard, 3: impossible}
        else:
            def easy():
                game = Game(600, 600, 15, 3, 300, 2)
                self.active = False
                game.run_game()

            def medium():
                game = Game(600, 600, 15, 3, 200, 1)
                self.active = False
                game.run_game()

            def hard():
                game = Game(600, 600, 15, 3, 100, 1)
                self.active = False
                game.run_game()

            def impossible():
                game = Game(600, 600, 15, 3, 50, 1)
                self.active = False
                game.run_game()

            functions = {0: easy, 1: medium, 2: hard, 3: impossible}

        for i in range(len(self.texts)):
            y_center = (0.25 * self.height + height * (0.5 + i))
            if (x_center - width / 2 < self.x < x_center + width / 2 and
                    y_center - height2 / 2 < self.y < y_center + height2 / 2):
                functions[i]()

    def create_buttons(self):
        height = self.height/(2*len(self.texts))
        for i in range(len(self.texts)):
            # Buttons will be from the 1/4 to 3/4, each of a bit less than what would make them cover that whole region.
            self.create_button(self.width/2, (0.25*self.height + height*(0.5 + i)),
                               0.4*self.width, 0.95*height, self.texts[i + 1], (155, 155, 155))

    def create_button(self, x_center, y_center, width, height, text, color, text_font="Arial", text_size=25,
                      text_color=(0, 0, 0)):
        if (x_center - width/2 < self.x < x_center + width/2 and
                y_center - height/2 < self.y < y_center + height/2):
            darker_color = (0.7*color[0], 0.7*color[1], 0.7*color[2])
            pygame.draw.rect(self.screen, darker_color, (x_center - width/2, y_center - height/2, width, height))
        else:
            pygame.draw.rect(self.screen, color, (x_center - width/2, y_center - height/2, width, height))

        font = pygame.font.SysFont(text_font, text_size)
        text1 = font.render(text, True, text_color)

        text_rect = text1.get_rect(center=(x_center, y_center))
        self.screen.blit(text1, text_rect)


menu = Menu(menu_type="MainMenu")


