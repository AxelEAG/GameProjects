import random
import pygame

pygame.init()
screen_height = 480
screen_width = 600
size = (screen_width, screen_height)

height = 40
width = 40
prob = 0.80

pixel_height = screen_height / height
pixel_width = 0.8 * screen_width / width


def random_state(height, width, prob):
    board_state = dead_state(height, width)

    board_state = randomize(board_state, prob)
    return board_state


def randomize(board, prob):
    for i in range(len(board)):
        for j in range(len(board[i])):
            random_number = random.random()
            if random_number >= prob:
                board[i][j] = 1
            else:
                board[i][j] = 0
    return board


def dead_state(height, width):
    board_state = [[0 for i in range(width)] for j in range(height)]
    return board_state


def next_board_state(board):
    board2 = [row[:] for row in board]

    for i in range(len(board)):
        for j in range(len(board[i])):
            count = check_surroundings(i, j, board)
            update_status(i, j, board2, count)
    return board2


def check_surroundings(i, j, board):
    height = len(board)
    width = len(board[0])

    count = 0
    if j == width - 1:
        count += board[i][j - 1]
        if i == height - 1:
            count += board[i - 1][j - 1]
            count += board[i - 1][j]
        elif i == 0:
            count += board[i + 1][j - 1]
            count += board[i + 1][j]
        else:
            count += board[i - 1][j - 1]
            count += board[i - 1][j]
            count += board[i + 1][j - 1]
            count += board[i + 1][j]
    elif j == 0:
        count += board[i][j + 1]
        if i == height - 1:
            count += board[i - 1][j]
            count += board[i - 1][j + 1]
        elif i == 0:
            count += board[i + 1][j]
            count += board[i + 1][j + 1]
        else:
            count += board[i - 1][j]
            count += board[i - 1][j + 1]
            count += board[i + 1][j]
            count += board[i + 1][j + 1]
    else:
        count += board[i][j - 1]
        count += board[i][j + 1]

        if i == height - 1:
            count += board[i - 1][j - 1]
            count += board[i - 1][j]
            count += board[i - 1][j + 1]
        elif i == 0:
            count += board[i + 1][j - 1]
            count += board[i + 1][j]
            count += board[i + 1][j + 1]
        else:
            count += board[i - 1][j - 1]
            count += board[i - 1][j]
            count += board[i - 1][j + 1]
            count += board[i + 1][j - 1]
            count += board[i + 1][j]
            count += board[i + 1][j + 1]

    return count


def update_status(i, j, board2, count):
    cell = board2[i][j]
    if count < 2:
        cell = 0
    if count > 3:
        cell = 0
    if count == 3 and cell == 0:
        cell = 1

    board2[i][j] = cell


def run_game():
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("The Game Of Life")

    clean_screen(screen)
    board = dead_state(width, height)

    new_cycle_event = pygame.USEREVENT + 1
    pygame.time.set_timer(new_cycle_event, 1000)

    start = False
    running = True
    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if start == True and event.type == new_cycle_event:
                for x in range(width):
                    for y in range(height):
                        pygame.draw.rect(screen, (150 * (1 - board[x][y]), 150, 150 * (1 - board[x][y])),
                                         (x * pixel_width, y * pixel_height, pixel_width,
                                          pixel_height))  # (x, y, width, height)
                        pygame.draw.rect(screen, (0, 0, 0),
                                         (x * pixel_width, y * pixel_height, pixel_width,
                                          pixel_height), width=1)
                if board == dead_state(height, width):
                    start = False
                board = next_board_state(board)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = mouse[0]
                y = mouse[1]
                if 485 < x < 595 and 10 < y < 50 and start == False:
                    if board != dead_state(height, width):
                        start = True
                if 485 < x < 595 and 60 < y < 100 and start == True:
                    start = False
                if 485 < x < 595 and 110 < y < 150:
                    clean_screen(screen)
                    board = random_state(height, width, prob)
                    start = True
                if 485 < x < 595 and 160 < y < 200:
                    board = dead_state(width, height)
                    clean_screen(screen)
                    start = False
                if 485 < x < 595 and 210 < y < 250:
                    pygame.quit()
                if 0 < x < 480 and 0 < y < 480 and start == False:
                    i = int(x/pixel_width)
                    j = int(y/pixel_height)
                    board[i][j] = 1 - board[i][j]
                    pygame.draw.rect(screen, (150 * (1 - board[i][j]), 150, 150 * (1 - board[i][j])),
                                     (i*pixel_width, j*pixel_height, pixel_width, pixel_height))
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (i*pixel_width, j*pixel_height, pixel_width, pixel_height), width=1)

        create_buttons(mouse, screen)

        pygame.display.flip()



def create_buttons(mouse, screen):
    if 485 < mouse[0] < 595 and 10 < mouse[1] < 50:
        pygame.draw.rect(screen, (255, 255, 255), (485, 10, 110, 40))
    else:
        pygame.draw.rect(screen, (155, 155, 155), (485, 10, 110, 40))

    if 485 < mouse[0] < 595 and 60 < mouse[1] < 100:
        pygame.draw.rect(screen, (255, 255, 255), (485, 60, 110, 40))
    else:
        pygame.draw.rect(screen, (155, 155, 155), (485, 60, 110, 40))

    if 485 < mouse[0] < 595 and 110 < mouse[1] < 150:
        pygame.draw.rect(screen, (255, 255, 255), (485, 110, 110, 40))
    else:
        pygame.draw.rect(screen, (155, 155, 155), (485, 110, 110, 40))

    if 485 < mouse[0] < 595 and 160 < mouse[1] < 200:
        pygame.draw.rect(screen, (255, 255, 255), (485, 160, 110, 40))
    else:
        pygame.draw.rect(screen, (155, 155, 155), (485, 160, 110, 40))
    if 485 < mouse[0] < 595 and 210 < mouse[1] < 250:
        pygame.draw.rect(screen, (255, 255, 255), (485, 210, 110, 40))
    else:
        pygame.draw.rect(screen, (155, 155, 155), (485, 210, 110, 40))

    font = pygame.font.SysFont('Arial', 25)
    text1 = font.render('START', True, (0, 0, 0))
    text2 = font.render('STOP', True, (0, 0, 0))
    text3 = font.render('RANDOM', True, (0, 0, 0))
    text4 = font.render('CLEAN', True, (0, 0, 0))
    text5 = font.render('QUIT', True, (0, 0, 0))

    screen.blit(text1, (505, 15))
    screen.blit(text2, (515, 65))
    screen.blit(text3, (495, 115))
    screen.blit(text4, (505, 165))
    screen.blit(text5, (515, 215))


def clean_screen(screen):
    for x in range(width):
        for y in range(height):
            pygame.draw.rect(screen, (150, 150, 150),
                             (x * pixel_width, y * pixel_height, pixel_width,
                              pixel_height))  # (x, y, width, height)
            pygame.draw.rect(screen, (0, 0, 0),
                             (x * pixel_width, y * pixel_height, pixel_width,
                              pixel_height), width=1)

run_game()

