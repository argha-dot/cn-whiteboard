import sys
import os
import time

import pygame
from pygame.locals import *

pygame.init()

win_wt, win_ht = 800, 600
fps_clock = pygame.time.Clock()
fps = 300

win = pygame.display.set_mode((win_wt, win_ht))
font = pygame.font.SysFont("Arial", 15)

WHITE = "#ffffff"
BLACK = "000000"
PIXEL_SIZE = 10

# ==========================================================================================

def terminate():
    pygame.quit()
    sys.exit()


def out_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()


def load_img(name):
    try:
        image = pygame.image.load(fullname(name))
    except pygame.error as e:
        print("Can't load image:", name)
        raise SystemExit(e)
    return image


def fullname(name):
    return os.path.join("data", name)


def delay(j):
    i = 0
    while i < j:
        pygame.time.wait(50)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                i = j + 1
                terminate()


def update_fps():
    fps = str(int(fps_clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


# ==========================================================================================


class Cursor(object):
    def __init__(self):
        self.color = pygame.Color("#000000")
        self.size = 4

    def get_grid_pos(self, pos):
        x, y = pos

        row = y // PIXEL_SIZE
        col = x // PIXEL_SIZE

        return row, col

    def draw(self):
        pygame.draw.circle(win, self.color, (pygame.mouse.get_pos()), self.size)


class Board():
    def __init__(self):
        self.x = int(win_wt / PIXEL_SIZE)
        self.y = int(win_ht / PIXEL_SIZE)
        self.board = [["#ffffff" for x in range(self.x)] for y in range(self.y)]

    def draw_grid(self):
        for i in range(self.y):
            pygame.draw.line(win, pygame.Color(40, 40, 40), (0, i * PIXEL_SIZE), (win_wt, i * PIXEL_SIZE))

        for i in range(self.x):
            pygame.draw.line(win, pygame.Color(40, 40, 40), (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, win_ht))

        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                pygame.draw.rect(win, pygame.Color(row[j]), (j * PIXEL_SIZE + 1, i * PIXEL_SIZE + 1, PIXEL_SIZE - 1, PIXEL_SIZE - 1))

    def color_grid(self, pos, color):
        self.board[pos[0]][pos[1]] = color


def main():

    def run_game():
        last_time = time.time()
        cursor = Cursor()
        board = Board()
        win.fill(pygame.Color(WHITE))

        while True:
            dt = time.time() - last_time
            dt *= 120
            last_time = time.time()

            board.draw_grid()

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    terminate()
                if pygame.mouse.get_pressed()[0]:
                    board.color_grid(cursor.get_grid_pos(pygame.mouse.get_pos()), "#000000")


            win.blit(update_fps(), (0, 0))
            pygame.display.update()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
