import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pickle
import sys
import time
import threading

import pygame
import pygame.gfxdraw

from _game.cursor import Cursor
from _game.board import Board
from _game.button import Button
from _game.misc import update_fps
from _game.vars import PIXEL_SIZE, WIN_HT, WIN_WT

from client import Client_Network


WHITE       = "#ffffff"
BLACK       = "#000000"
RED         = "#ff0000"
BLUE        = "#0000ff"
GREEN       = "#00ff00"
TURQUOISE   = "#40e0d0"

def change_board(board):
    net_recv = Client_Network()
    net_recv.connect()

    connected = True
    while connected:
        msg = pickle.loads(net_recv.client.recv(4096 * 8))
        if type(msg) == str:
            print(msg)
            if msg == 'q':
                connected = False
                net_recv.disconnect()
        else:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    board[i][j] = msg[i][j]


def main():
    name = input("Enter a name: ").strip()
    pygame.init()

    fps_clock = pygame.time.Clock()
    fps = 300

    win = pygame.display.set_mode((WIN_WT, WIN_HT))
    font = pygame.font.SysFont("Arial", 15)

    pygame.display.set_caption("Whiteboard")
    pygame.display.set_caption(name)

    net = Client_Network()
    net.connect()
    net.send("Hello", pick=True)

    def run_game():
        last_time = time.time()
        cursor = Cursor(win)
        board = Board(win)
        win.fill(pygame.Color(WHITE))

        buttons = [
                Button(win, WIN_WT - 100, 50,  RED),
                Button(win, WIN_WT - 130, 50,  BLUE),
                Button(win, WIN_WT - 100, 80,  GREEN),
                Button(win, WIN_WT - 130, 80,  BLACK),
                Button(win, WIN_WT - 100, 110, WHITE),
                Button(win, WIN_WT - 130, 110, TURQUOISE),
            ]

        test = threading.Thread(target=change_board, args=([board.board]), daemon=True)
        test.start()

        while True:
            dt = time.time() - last_time
            dt *= 120
            last_time = time.time()

            board.draw_grid()
            
            for button in buttons:
                button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    net.send("q", pick=True)
                    net.disconnect()

                    pygame.quit()
                    sys.exit()

                if pygame.mouse.get_pressed()[0]:
                    board.color_grid(cursor.get_grid_pos(pygame.mouse.get_pos()), cursor.color)
                    for button in buttons:
                        button.change_color(cursor)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    net.send(board.board, pick=True)

            win.blit(update_fps(fps_clock, font), (0, 0))
            pygame.display.update()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
