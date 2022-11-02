# External imports
import pygame as pg
from sys import exit

# Internal imports

class MenuPage:

    def __init__(self, board):
        self.board = board

        # Texts
        self.head_text = 2

        # Buttons
        self.quit_button = 3

    def update(self):
        for event in pg.events.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    continue
                elif event.button == 3:
                    continue
        return 2
