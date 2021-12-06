import sys
import pygame

from _game.vars import PIXEL_SIZE, WIN_HT, WIN_WT



class Board():
    def __init__(self, surface):
        self.x = int(WIN_WT / PIXEL_SIZE)
        self.y = int(WIN_HT / PIXEL_SIZE)
        self.board = [["#ffffff" for x in range(self.x)] for y in range(self.y)]
        self.surface = surface
        print(sys.getsizeof(self.board))


    def draw_grid(self):
        for i in range(self.y):
            pygame.gfxdraw.hline(self.surface, 0, WIN_WT, i * PIXEL_SIZE, pygame.Color(40, 40, 40))

        for i in range(self.x):
            pygame.gfxdraw.vline(self.surface, i * PIXEL_SIZE, 0, WIN_HT, pygame.Color(40, 40, 40))

        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                pygame.draw.rect(self.surface, pygame.Color(row[j]), (j * PIXEL_SIZE + 1, i * PIXEL_SIZE + 1, PIXEL_SIZE - 1, PIXEL_SIZE - 1))

    def color_grid(self, pos, color):
        self.board[pos[0]][pos[1]] = color
