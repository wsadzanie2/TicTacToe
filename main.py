import sys
import random
import time

visuals = True
if visuals:
    import pygame
    from pygame.locals import *

    pygame.init()

    font = pygame.font.SysFont('', 64)

    screen = pygame.display.set_mode((1200, 900), RESIZABLE)

    pygame.display.set_caption('TicTacToe!')

run = True

board = [None for _ in range(9)]

size = 300

player = 1

bot_player = 2

start_time = time.time()

mode = 'bot'

if not visuals:
    mode = 'bots'

wins, losses, draws = 0, 0, 0

lost_state = []


def reverseEnum(data: list):
    for i in range(len(data) - 1, -1, -1):
        yield i, data[i]


def convert_number_to_string(number: int, precision=0):
    endings = ['', 'k', 'mln', 'mld']
    for index, value in reverseEnum(endings):
        if index == 0:
            return str(round(number, precision))
        if number >= 1000 ** index:
            if precision == 0:
                return f'{int(number / (1000 ** index))}{value}'
            return f'{round(number / (1000 ** index), precision)}{value}'


class Button:
    def __init__(self, func=lambda: None):
        self.rect = pygame.Rect(size * 3, 150, 150, 50)
        self.func = func
        self.y = 150
        self.color_a = (100, 100, 100)
        self.color_b = (0, 100, 100)
        self.color_c = (0, 90, 90)
        self.text = None

    def draw(self):
        if not visuals:
            return
        global mode
        # update position
        self.rect = pygame.Rect(size * 3, self.y, 150, 50)
        if mode == 'bot':
            pygame.draw.rect(screen, self.color_a, self.rect)
        elif mode == 'players':
            pygame.draw.rect(screen, self.color_b, self.rect)
        else:
            pygame.draw.rect(screen, self.color_c, self.rect)
        if self.text is not None:
            screen.blit(font.render(self.text, False, (0, 0, 0)), (self.rect.x, self.rect.y))

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.func(self)


def draw_x(x, y, width, height, thiccness=1):
    for i in range(5):
        pygame.draw.line(screen, "blue", (x + i, y), (width + x + i, height + y), thiccness)
        pygame.draw.line(screen, "blue", (width + x + i, y), (x + i, height + y), thiccness)


def draw_board():
    if visuals:
        # draw actual board
        for bx in range(3):
            for by in range(3):
                if (bx + by) % 2 == 1:
                    color = (50, 50, 50)
                else:
                    color = (60, 60, 60)
                pygame.draw.rect(screen, color, pygame.Rect(bx * size, by * size, size, size))

        # draw circles and squares
        for index, square in enumerate(board):

            x = index % 3
            y = index // 3
            if square == 1:
                # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(SIZE * x, SIZE * y, SIZE, SIZE))
                draw_x(size * x, size * y, size, size, 10)
            elif square == 2:
                pygame.draw.circle(screen, (0, 255, 0), (size * x + (size // 2), size * y + (size // 2)), (size // 2))


def two_out_of_three_and_not_None(a: int, b: int, c: int):
    return (a == b is not None) or (b == c is not None) or (c == a is not None)


def check_draw():
    for box in board:
        if box is None:
            return False
    return True


def check_win():
    # check for a draw
    if check_draw():
        return 'draw'

    # rows
    for row in range(3):
        if board[row * 3] == board[row * 3 + 1] == board[row * 3 + 2]:
            if board[row * 3] is not None:
                return board[row * 3]
    # columns
    for column in range(3):
        if board[column] == board[column + 3] == board[column + 6]:
            if board[column] is not None:
                return board[column]
    # diagonals
    if board[0] == board[4] == board[8] and board[0] is not None:
        return board[0]
    if board[2] == board[4] == board[6] and board[2] is not None:
        return board[2]


def handle_presses(event):
    if visuals:
        global player, board, winner
        if event.type == MOUSEBUTTONDOWN:
            if winner is not None:
                board = [None for _ in range(9)]
                winner = None
                return
            x, y = pygame.mouse.get_pos()
            x = x // size
            y = y // size
            if x >= 3 or x < 0:
                return
            if y >= 3 or y < 0:
                return
            index = 3 * y + x
            if board[index] is None:
                board[index] = player
                player %= 2
                player += 1


def check_edges():
    for value in range(4):
        if board[1 + (2 * value)] is None:
            return 1 + (2 * value)
    return False


def check_corners():
    if board[0] is None:
        return 0
    if board[8] is None:
        return 8
    if board[6] is None:
        return 6
    if board[2] is None:
        return 2

    return False

def handle_num_key(event, key, poz):
    global player
    if event.key == key:
        if board[poz] is None and (player != bot_player or mode == 'players') and mode in ('players', 'bot'):
            board[poz] = player
            player %= 2
            player += 1


def handle_numpad(event):
    if event.type == KEYDOWN:
        handle_num_key(event, K_KP1, 6)
        handle_num_key(event, K_KP2, 7)
        handle_num_key(event, K_KP3, 8)
        handle_num_key(event, K_KP4, 3)
        handle_num_key(event, K_KP5, 4)
        handle_num_key(event, K_KP6, 5)
        handle_num_key(event, K_KP7, 0)
        handle_num_key(event, K_KP8, 1)
        handle_num_key(event, K_KP9, 2)

def check_rows():
    for row in [1, 0, 2]:
        if two_out_of_three_and_not_None(board[row * 3], board[row * 3 + 1], board[row * 3 + 2]):
            for value in range(3):
                if board[row * 3 + value] is None:
                    return row * 3 + value

def check_columns():
    for column in [1, 0, 2]:
        if two_out_of_three_and_not_None(board[column], board[column + 3], board[column + 6]):
            for value in range(3):
                if board[column + (3 * value)] is None:
                    return column + (3 * value)

def bot():
    priority = 'corner'
    value = check_rows()
    if value is not None:
        return value
    value = check_columns()
    if value is not None:
        return value

    # diagonals
    if two_out_of_three_and_not_None(board[0], board[4], board[8]):
        for value in range(3):
            if board[value * 4] is None:
                return value * 4
        if board[0] == board[8]:
            priority = 'edge'

    if two_out_of_three_and_not_None(board[2], board[4], board[6]):
        for value in range(3):
            if board[(value * 2) + 2] is None:
                return (value * 2) + 2
        if board[2] == board[6]:
            priority = 'edge'
    # middle
    if board[4] is None:
        return 4

    # corner traps
    if board[1] is not None:
        if board[3] == board[1]:
            if board[0] is None:
                return 0
        if board[5] == board[1]:
            if board[2] is None:
                return 2
    if board[7] is not None:
        if board[3] == board[7]:
            if board[4] is None:
                return 4
        if board[5] == board[7]:
            if board[8] is None:
                return 8

    # corner-edge traps
    if board[5] == board[6]:
        if board[5] is not None:
            if board[8] is None:
                return 8
    if board[2] == board[7] and board[2] is not None:
        if board[8] is None:
            return 8

    # nice way to win
    if board[3] == board[8] and board[3] is not None:
        if board[2] is None and board[0] is not None:
            return 2

    if priority == 'edge':
        value = check_edges()
        if value:
            return value
        value = check_corners()
        if value is not False:
            return value
    elif priority == 'corner':
        value = check_corners()
        if value is not False:
            return value
        value = check_edges()
        if value:
            return value

    return random.randint(0, 8)


def random_bot():
    while winner is None:
        value = random.randint(0, 8)
        if board[value] is None:
            return value


### BUTTON STUFF ###


def button_func(self):
    global mode, board, wins, draws, losses
    board = [None for _ in range(9)]
    wins, draws, losses = 0, 0, 0
    if mode == 'bot':
        mode = 'players'
        self.text = 'player'
    elif mode == 'players':
        mode = 'bot'
        self.text = 'bot'


button = Button(button_func)
button.text = 'bot'

def turn_off_ui_function(self):
    global visuals, mode, board, winner, start_time
    visuals = False
    pygame.quit()
    if mode != 'bots':
        start_time = time.time()
        mode = 'bots'
        board = [None for _ in range(9)]
        winner = None


turn_off_ui_button = Button(turn_off_ui_function)
turn_off_ui_button.y = 210
turn_off_ui_button.color_b = turn_off_ui_button.color_a
turn_off_ui_button.text = 'TUI'

clock = pygame.time.Clock()

while run:
    if visuals:
        dt = clock.tick()
        screen.fill((75, 75, 75))
        draw_board()
        button.draw()
        turn_off_ui_button.draw()
    winner = check_win()
    if visuals:
        # this variables are for the bot. We want to see data for you!
        for index, thingy in enumerate([f'wins: {losses}', f'draws: {draws}', f'losses: {wins}']):
            font_thingy = font.render(thingy, False, (0, 0, 0))
            screen.blit(font_thingy, (size * 3, 40 * index))

    if winner is not None:
        if winner == (bot_player % 2 + 1):
            # pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(0, 0, SIZE * 3.2, SIZE * 3.2))
            if visuals:
                screen.fill((0, 0, 255))
            losses += 1
            lost_state = board.copy()
            board = [None for _ in range(9)]
        elif winner == bot_player:
            # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, SIZE * 3.2, SIZE * 3.2))
            if visuals:
                screen.fill((0, 255, 0))
            wins += 1
            board = [None for _ in range(9)]

        elif winner == 'draw':
            draws += 1
            board = [None for _ in range(9)]
        if mode == 'bots':
            print(f'--------({convert_number_to_string(wins + losses + draws, 2)})--------')
            try:
                print(f'GPS: {convert_number_to_string(int(wins + losses + draws) / (time.time() - start_time), 3)}')
            except ZeroDivisionError:
                print(f'GPS: ')
            print(f'wins: {convert_number_to_string(wins)}')
            print(f'draws: {convert_number_to_string(draws)}')
            print(f'losses: {convert_number_to_string(losses)}')
            if losses > 0:
                print(lost_state[:3])
                print(lost_state[3:6])
                print(lost_state[6:9])
                sys.exit()
            winner = check_win()
    else:
        if player == bot_player and mode in ('bot', 'bots'):
            bot_move = bot()
            if board[bot_move] is None:
                board[bot_move] = player
                player %= 2
                player += 1
        elif mode == 'bots':
            bot_move = random_bot()
            if board[bot_move] is None:
                board[bot_move] = player
                player %= 2
                player += 1
            else:
                print(bot_move)
                print(board[:3])
                print(board[3:6])
                print(board[6:9])
    if visuals:
        for event in pygame.event.get():
            if event.type == QUIT:
                print(lost_state)
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                x, y = screen.get_size()
                size = min(x, y) // 3
            handle_presses(event)
            button.update(event)
            turn_off_ui_button.update(event)
            handle_numpad(event)
        if visuals:
            pygame.display.flip()
