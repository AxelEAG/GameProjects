import random


def render(board):
    print('   ', *[col for col in range(board.size)])
    print('  ' + "-" * (3 + 2 * board.size))
    for row in range(board.size):
        print(row, "|", *[board.getValue(col, row) for col in range(board.size)], "|")

    print('  ' + "-" * (3 + 2 * board.size))


def get_move(board):
    x = int(input("What is your x coordinate?: "))
    y = int(input("What is your y coordinate?: "))

    while not board.isValid(x, y) or board.isOccupied(x, y):
        print("Sorry, please enter a valid coordinate.")
        render(board)
        x = int(input("What is your x coordinate?: "))
        y = int(input("What is your y coordinate?: "))

    return x, y


def won_game(board):
    for i in range(board.size):
        first = board.getValue(0, i)
        if first == ' ':
            continue

        if board.state[i].count(first) == board.size:
            return first

    for j in range(board.size):
        first = board.getValue(j, 0)
        if first == ' ':
            continue

        for i in range(1, board.size):
            if first != board.getValue(j, i):
                break
        else:
            return first

    diag1 = True
    diag2 = True
    first = board.getValue(0, 0)
    last = board.getValue(board.size - 1, 0)
    for i in range(board.size):
        if first != ' ':
            if board.getValue(i, i) != first:
                diag1 = False
        else:
            diag1 = False
        if last != ' ':
            if board.getValue(i, board.size-i - 1) != last:
                diag2 = False
        else:
            diag2 = False
    if diag1:
        return first
    elif diag2:
        return last

    return None


def change_turn(turn):
    if turn == 'X':
        return 'O'
    else:
        return 'X'


def select_bot():
    bots = {1: human_player, 2: random_ai, 3: finds_winning_moves_ai, 4: finds_winning_and_losing_moves_ai,
            5: minimax_saved_cache_ai}
    print("Available bots are: 1- human, 2- random, 3-findsWin, 4-findsLoseToo, 5-Minimax")
    print("Write the number to select them. 'X' starts!")
    ai1 = int(input("Choose the first bot: "))
    ai2 = int(input("Choose the second bot: "))

    ais = {"X": bots[ai1], "O": bots[ai2]}
    return ais


def get_legal_moves(board):
    coordinates = {1:[0, 0], 2:[1, 0], 3:[2, 0], 4:[0, 1], 5:[1, 1],6:[2, 1], 7:[0, 2], 8:[1, 2],9:[2, 2]}
    available = []
    for i in range(1, board.size ** 2 + 1):
        x, y = coordinates[i]
        if not board.isOccupied(x, y):
            available.append(coordinates[i])
    return available


def minimax_score(board, player, cache):
    won = won_game(board)

    if won is not None:
        if won == "X":
            return 10
        else:
            return -10

    if board.isFull():
        return 0

    legal_moves = get_legal_moves(board)
    scores = []
    for x, y in legal_moves:
        new_board = board.setValue(x, y, player)
        opponent = change_turn(player)

        string = turn_string(new_board)

        if string not in cache:
            score = minimax_score(new_board, opponent, cache)
            cache[string] = score
        scores.append(cache[string])

    if player == "X":
        return max(scores)
    else:
        return min(scores)


def save_minimax():
    board = Board()
    player = "X"
    moves = get_legal_moves(board)
    scores = []

    cache = {}

    for x, y in moves:
        new_board = board.setValue(x, y, player)
        opponent = change_turn(player)
        string = turn_string(new_board)

        if string not in cache:
            score = minimax_score(new_board, opponent, cache)
            cache[string] = score
        scores.append(cache[string])

    file = open("minimax.csv", "w")
    for key in cache:
        file.write(f"{key},{cache[key]}\n")


def turn_string(board):
    string = ""
    for row in board.state:
        for element in row:
            string += element
    return string


def create_cache():
    cache = {}
    board = Board()
    str_board = turn_string(board)

    coordinates = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    for i in range(1, board.size ** 2 + 1):
        x, y = coordinates[i]
    return cache


class Board:
    def __init__(self):
        self.size = 3
        self.state = [[' ']*self.size for i in range(self.size)]

    def getValue(self, x, y):
        return self.state[y][x]

    def setValue(self, x, y, val):
        board2 = Board()
        board2.state = [row[:] for row in self.state]

        board2.state[y][x] = val
        return board2

    def isValid(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return True
        else:
            return False

    def isOccupied(self, x, y):
        if self.state[y][x] != ' ':
            return True
        else:
            return False

    def isFull(self):
        full = True
        for x in range(self.size):
            for y in range(self.size):
                if self.getValue(x, y) == ' ':
                    full = False
                    break
            if not full:
                break
        return full


def random_ai(board, player):
    coordinates = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    available = []
    for i in range(1, board.size**2 + 1):
        x, y = coordinates[i]
        if not board.isOccupied(x, y):
            available.append(i)

    move = coordinates[random.choice(available)]
    return move


def finds_winning_moves_ai(board, player):
    coordinates = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    available = []
    for i in range(1, board.size ** 2 + 1):
        x, y = coordinates[i]
        if not board.isOccupied(x, y):
            available.append(i)
            won = won_game(board.setValue(x, y, player))

            if won is not None:
                move = [x, y]
                return move

    move = coordinates[random.choice(available)]
    return move


def finds_winning_and_losing_moves_ai(board, player):
    coordinates = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [0, 1], 5: [1, 1], 6: [2, 1], 7: [0, 2], 8: [1, 2], 9: [2, 2]}
    available = []
    for i in range(1, board.size ** 2 + 1):
        x, y = coordinates[i]
        if not board.isOccupied(x, y):
            available.append(i)
            won = won_game(board.setValue(x, y, player))

            if won is not None:
                move = [x, y]
                return move

    for i in available:
        x, y = coordinates[i]
        won = won_game(board.setValue(x, y, change_turn(player)))

        if won is not None:
            move = [x, y]
            return move

    move = coordinates[random.choice(available)]
    return move


def human_player(board, player):
    x = int(input("What is your x coordinate?: "))
    y = int(input("What is your y coordinate?: "))

    while not board.isValid(x, y) or board.isOccupied(x, y):
        print("Sorry, please enter a valid coordinate.")
        render(board)
        x = int(input("What is your x coordinate?: "))
        y = int(input("What is your y coordinate?: "))

    return x, y


def minimax_cache_ai(board, player):
    moves = get_legal_moves(board)
    scores = []

    cache = {}

    for x, y in moves:
        new_board = board.setValue(x, y, player)
        opponent = change_turn(player)
        string = turn_string(new_board)

        if string not in cache:
            score = minimax_score(new_board, opponent, cache)
            cache[string] = score
        scores.append(cache[string])

    winning = []
    if player == "X":
        highest = max(scores)
    else:
        highest = min(scores)

    for i in range(len(moves)):
        if scores[i] == highest:
            winning.append(moves[i])

    move = random.choice(winning)
    return move


def minimax_saved_cache_ai(board, player):
    moves = get_legal_moves(board)
    scores = []

    cache = {}
    file = open("minimax.csv")
    for line in file.readlines():
        key, item = line.split(",")
        cache[key] = item[:-1]

    for x, y in moves:
        new_board = board.setValue(x, y, player)
        string = turn_string(new_board)
        scores.append(cache[string])

    winning = []
    if player == "X":
        highest = max(scores)
    else:
        highest = min(scores)

    for i in range(len(moves)):
        if scores[i] == highest:
            winning.append(moves[i])

    move = random.choice(winning)
    return move


def run_game(ais=None, repeated=False):
    board = Board()
    turn = "X"

    if ais is None:
        ais = select_bot()

    if not repeated:
        render(board)

    while True:
        x, y = ais[turn](board, turn)

        board = board.setValue(x, y, turn)
        turn = change_turn(turn)

        if not repeated:
            render(board)

        won = won_game(board)

        if won is not None:
            if not repeated:
                print(f"{won} won!")
            return won

        if board.isFull():
            if not repeated:
                print("It's a draw!")
            return None


def play(player1, player2, repeated=False):
    bots = {1: human_player, 2: random_ai, 3: finds_winning_moves_ai, 4: finds_winning_and_losing_moves_ai,
            5: minimax_saved_cache_ai}

    ais = {"X": bots[player1], "O": bots[player2]}

    return run_game(ais, repeated)


def repeated_battles(player1, player2, count, repeated):
    tally = {None: 0, "X": 0, "O": 0}
    for i in range(count):
        tally[play(player1, player2, repeated)] += 1

    return tally


# run_game()
# bots = {1: human_player, 2: random_ai, 3: finds_winning_moves_ai, 4: finds_winning_and_losing_moves_ai,
#             5: minimax_ai, 6: minimax_saved_cache_ai}

# save_minimax()

# repeated_battles(5, 2, 1000, True)













