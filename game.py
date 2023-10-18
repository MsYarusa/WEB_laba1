import pygame as pg
from random import choice
from math import floor
import time
import os

WIDTH = 520
HEIGHT = 520
SIZE = (WIDTH, HEIGHT)
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

mouse_events = []
space_clicked = False
buff_screen = pg.Surface(SIZE)
need_to_send_screen = True


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[-2] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

        self.mines_amount = 10
        self.clicked_count = 0
        self.game_is_over = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_mines_amount(self, amount):
        self.mines_amount = amount

    def render(self, screen):
        for j in range(self.height):
            for i in range(self.width):
                pg.draw.rect(screen, (255, 255, 255), (
                    self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size, self.cell_size), 1)

    def place_mines(self):

        possible_mines = []

        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                possible_mines.append((j, i))

        mines = []

        for i in range(self.mines_amount):
            mine = choice(possible_mines)
            possible_mines.remove(mine)
            mines.append(mine)

        for i in range(self.mines_amount):
            x = mines[i][0]
            y = mines[i][1]
            self.board[x][y] = -1

    def restart(self, screen):
        self.board = [[-2] * self.width for _ in range(self.height)]

        screen.fill((0, 0, 0))
        self.render(screen)

        self.place_mines()

        self.clicked_count = 0
        self.game_is_over = False

    def end_game(self, screen, lost):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == -1:
                    pg.draw.rect(screen, (255, 0, 0), (
                        self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size))

        time.sleep(0.5)
        shadow = pg.Surface(SIZE)
        shadow.fill((0, 0, 0))
        shadow.set_alpha(170)
        screen.blit(shadow, (0, 0))

        if lost:
            text = 'БААБАААХ...'
        else:
            text = 'ПОБЕДА?!?!?!?'

        label_font = pg.font.SysFont('calibry', 50)
        text_rendered = label_font.render(text, 0, pg.Color('white'))
        text_rect = text_rendered.get_rect()
        text_rect.centerx = WIDTH // 2
        text_rect.centery = HEIGHT // 2 - 20
        screen.blit(text_rendered, text_rect)

        label_font = pg.font.SysFont('calibry', 24)
        text_rendered = label_font.render('Нажмите пробел, чтобы начать сначала', 0, pg.Color('white'))
        text_rect = text_rendered.get_rect()
        text_rect.centerx = WIDTH // 2
        text_rect.centery = HEIGHT - 30
        screen.blit(text_rendered, text_rect)

    def on_click(self, cell_coords, screen):
        x = cell_coords[0]
        y = cell_coords[1]

        if self.board[x][y] == -1:
            self.game_is_over = True
            self.end_game(screen, True)
            return

        if self.board[x][y] != -2:
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

        self.clicked_count += 1
        if (self.clicked_count + self.mines_amount) == 100:
            self.game_is_over = True
            self.end_game(screen, False)

    def get_cell(self, mouse_pos):

        x = floor((int(mouse_pos[0]) - self.left) / self.cell_size)
        y = floor((int(mouse_pos[1]) - self.top) / self.cell_size)

        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        else:
            return None

    def get_click(self, mouse_pos, screen):
        cell = self.get_cell(mouse_pos)

        if not (cell is None):
            self.on_click(cell, screen)


def sapper(ip):
    pg.init()

    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption(ip)
    screen.fill((0, 0, 0))
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    board.set_view(10, 10, 50)
    board.render(screen)
    board.place_mines()

    running = True
    while running:
        global need_to_send_screen, space_clicked

        if mouse_events:
            for pos in mouse_events:
                if not board.game_is_over:
                    board.get_click(pos, screen)
                need_to_send_screen = True
                mouse_events.remove(pos)

        if space_clicked:
            space_clicked = False
            if board.game_is_over:
                board.restart(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("[СЕРВЕР ВЫКЛЮЧЕН]")
                pg.quit()
                os.abort()

        if need_to_send_screen:
            buff_screen.blit(screen, (0, 0))
            time.sleep(0.01)

        pg.display.flip()