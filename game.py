import pygame as pg
from random import choice
from math import floor
import time

WIDTH = 520
HEIGHT = 520
SIZE = (WIDTH, HEIGHT)
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

buffer = []
buff_screen = pg.Surface(SIZE)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for j in range(self.height):
            for i in range(self.width):
                pg.draw.rect(screen, (255, 255, 255), (
                    self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):

        x = floor((int(mouse_pos[0]) - self.left) / self.cell_size)
        y = floor((int(mouse_pos[1]) - self.top) / self.cell_size)

        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        else:
            return None

    def make_it_mine(self, cell_coords, screen):
        x = int(cell_coords[0])
        y = int(cell_coords[1])
        pg.draw.rect(screen, (255, 0, 0), (
            self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size))
        self.board[x][y] = -1

    def on_click(self, cell_coords, screen):
        x = cell_coords[0]
        y = cell_coords[1]
        if self.board[x][y] != 0:
            return

        mines = 0
        for delta_x in (-1, 0, 1):
            for delta_y in (-1, 0, 1):
                if 0 <= x + delta_x < self.width and 0 <= y + delta_y < self.height:
                    if self.board[x + delta_x][y + delta_y] == -1:
                        mines += 1

        font = pg.font.Font(None, self.cell_size // 2)
        text = font.render(str(mines), True, (255, 255, 255))
        text_x = self.left + x * self.cell_size + self.cell_size // 2 - text.get_width() // 2
        text_y = self.top + y * self.cell_size + self.cell_size // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))

    def get_click(self, mouse_pos, screen):
        cell = self.get_cell(mouse_pos)

        if not (cell is None):
            self.on_click(cell, screen)

flag = True

def semisapper(ip):
    pg.init()
    mines_count = 10

    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption(ip)
    screen.fill((0, 0, 0))
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    board.set_view(10, 10, 50)
    board.render(screen)

    possible_mines = []

    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            possible_mines.append((j, i))

    mines = []

    for i in range(mines_count):
        mine = choice(possible_mines)
        possible_mines.remove(mine)
        mines.append(mine)

    for i in range(mines_count):
        board.make_it_mine(mines[i], screen)

    running = True
    while running:
        global flag

        if buffer:
            for pos in buffer:
                board.get_click(pos, screen)
                flag = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if flag:
            buff_screen.blit(screen, (0, 0))
            time.sleep(0.01)

        pg.display.flip()