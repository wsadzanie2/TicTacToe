import sys
import pygame
import random
import time
from pygame.locals import *

pygame.init()

font = pygame.font.SysFont('', 64)

screen = pygame.display.set_mode((1200, 900), RESIZABLE)

run = True

board = [None for _ in range(9)]

size = 300

player = 1

bot_player = 2

mode = 'bot'

wins, losses, draws = 0, 0, 0

lost_state = []

class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 150, 50)
    def draw(self):
        global mode
        if mode == 'bot':
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
        else:
            pygame.draw.rect(screen, (0, 100, 100), self.rect)
    def update(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                global mode, board, wins, draws, losses
                board = [None for _ in range(9)]
                wins, draws, losses = 0, 0, 0
                if mode == 'bot':
                    mode = 'players'
                elif mode == 'players':
                    mode = 'bots'
                elif mode == 'bots':
                    mode = 'bot'

def draw_x(x, y, width, height, thiccness=1):
    for i in range(5):
        pygame.draw.line(screen, "blue", (x + i, y), (width + x + i, height + y), thiccness)
        pygame.draw.line(screen, "blue", (width + x + i, y), (x + i, height + y), thiccness)


def draw_board():
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
    # # top corners
    # for value in range(2):
    #     if board[value * 2] is None:
    #         return value * 2
    #
    # # bottom corners
    # for value in range(2):
    #     if board[6 + (value * 2)] is None:
    #         return 6 + (value * 2)
    if board[0] is None:
        return 0
    if board[8] is None:
        return 8
    if board[6] is None:
        return 6
    if board[2] is None:
        return 2

    return False
def bot():
    priority = 'corner'
    for row in range(3):
        if two_out_of_three_and_not_None(board[row * 3], board[row * 3 + 1], board[row * 3 + 2]):
            for value in range(3):
                if board[row * 3 + value] is None:
                    return row * 3 + value

    for column in range(3):
        if two_out_of_three_and_not_None(board[column], board[column + 3], board[column + 6]):
            for value in range(3):
                if board[column + (3 * value)] is None:
                    return column + (3 * value)

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
    if board[1] != 0:
        if board[3] == board[1]:
            if board[0] == 0:
                return 0
        if board[5] == board[1]:
            if board[0] == 0:
                return 0

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
    for row in range(3):
        if two_out_of_three_and_not_None(board[row * 3], board[row * 3 + 1], board[row * 3 + 2]):
            for value in range(3):
                if board[row * 3 + value] is None:
                    return row * 3 + value

    for column in range(3):
        if two_out_of_three_and_not_None(board[column], board[column + 3], board[column + 6]):
            for value in range(3):
                if board[column + (3 * value)] is None:
                    return column + (3 * value)

    # diagonals
    if two_out_of_three_and_not_None(board[0], board[4], board[8]):
        for value in range(3):
            if board[value * 4] is None:
                return value * 4

    if two_out_of_three_and_not_None(board[2], board[4], board[6]):
        for value in range(3):
            if board[(value * 2) + 2] is None:
                return (value * 2) + 2

    while winner is None:
        value = random.randint(0, 8)
        if board[value] is None:
            return value

button = Button(size * 3, 150)

while run:
    screen.fill((75, 75, 75))
    draw_board()
    button.draw()
    winner = check_win()
    for index, thingy in enumerate([f'wins: {wins}', f'draws: {draws}', f'losses: {losses}']):
        font_thingy = font.render(thingy, False, (0, 0, 0))
        screen.blit(font_thingy, (size * 3, 40 * index))

    if winner is not None:
        if winner == 1:
            # pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(0, 0, SIZE * 3.2, SIZE * 3.2))
            screen.fill((0, 0, 255))
            losses += 1
            lost_state = board.copy()
            board = [None for _ in range(9)]
        elif winner == 2:
            # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, SIZE * 3.2, SIZE * 3.2))
            screen.fill((0, 255, 0))
            wins += 1
            board = [None for _ in range(9)]

        elif winner == 'draw':
            draws += 1
            board = [None for _ in range(9)]
        if mode == 'bots':
            print('--------')
            print(wins)
            print(draws)
            print(losses)
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

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            x, y = screen.get_size()
            size = min(x, y) // 3
        handle_presses(event)
        button.update(event)
    pygame.display.flip()
