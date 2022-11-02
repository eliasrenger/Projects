# External imports
import pygame as pg
from sys import exit

# Internal imports
from Mine_sweeper.src.config import *
from Mine_sweeper.src.game_logic import *
from Packages.pg_gui_framework import *

class StartPage:

    def __init__(self, screen, board):
        self.screen = screen
        self.board = board


        # Colors
        self.light_background_clr = LIGHT_BACKGROUND_CLR
        self.background_clr = BACKGROUND_CLR
        self.dark_background_clr = DARK_BACKGROUND_CLR

        # Texts
        self.texts = []
        self.title = TITLE

        # Buttons
        self.buttons = []


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

        #display objects
        self.screen.blit((0,0), self.background_surf)

        for text in self.texts:
            text.display_text()

        for button in self.buttons:
            button.display_button()

        return 0