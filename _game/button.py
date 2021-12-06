import pygame


class Button(object):
    def __init__(self, surface, x, y, color):
        self.color = color
        self.size = 30
        self.surface = surface
        self.rect = pygame.Rect(x, y, self.size, self.size)


    def draw(self):
        pygame.draw.rect(self.surface, pygame.Color(self.color), [self.rect.x, self.rect.y, self.size, self.size])
        pygame.draw.rect(self.surface, pygame.Color("#000000"), [self.rect.x, self.rect.y, self.size, self.size], width=3)

    def change_color(self, cursor):
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            cursor.color = self.color

