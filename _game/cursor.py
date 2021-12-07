import pygame

from _game.vars import PIXEL_SIZE

class Cursor(object):
    def __init__(self, surface):
        self.color = "#000000"
        self.size = 4
        self.surface = surface

    def get_grid_pos(self, pos):
        x, y = pos

        row = y // PIXEL_SIZE
        col = x // PIXEL_SIZE

        return row, col

    def draw(self):
        pygame.draw.circle(self.surface, pygame.Color(self.color), (pygame.mouse.get_pos()), self.size)

