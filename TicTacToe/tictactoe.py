def render(board):
    print('   ', *[col for col in range(board.size)])
    print('  ' + "-" * (3 + 2 * board.size))
    for row in range(board.size):
        print(row, "|", *[board.getValue(col, row) for col in range(board.size)], "|")

    print('  ' + "-" * (3 + 2 * board.size))


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


class Board:
    def __init__(self):
        self.size = 3
        self.state = [[' ']*self.size for i in range(self.size)]

    def getValue(self, x, y):
        if self.isValid(x, y):
            return self.state[y][x]

    def setValue(self, x, y, val):
        if self.getValue(x, y) == ' ':
            if self.isValid(x, y) and not self.isOccupied(x, y):
                self.state[y][x] = val

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


def run_game():
    board = Board()
    render(board)

    turn = 'X'
    while True:
        x = int(input("What is your x coordinate?: "))
        y = int(input("What is your y coordinate?: "))

        if not board.isValid(x, y) or board.isOccupied(x, y):
            print("Sorry, please enter a valid coordinate.")
            render(board)
            continue

        board.setValue(x, y, turn)
        turn = change_turn(turn)

        render(board)

        won = won_game(board)

        if won is not None:
            print(f"{won} won!")
            break

        if board.isFull():
            print("It's a draw!")
            break


run_game()



