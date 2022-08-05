# External imports
import pygame as pg

# Internal imports
from src.config import *
from src.Astar_algorithm import Board
from src.Pages.StartPage import StartPage
from src.Pages.GridPage import GridPage
from src.Pages.InstructionsPage import InstructionsPage

"""
---Anteckningar---
Kraschar då inget input givits på någon minut på grund av rekursionsgräns
 - studera update()
"""

class GUI():
    """Class GUI codesfor the gui and updates the frames"""
    def __init__(self):
        """"""
        self.geometry = RES
        self.title = APP_TITLE

        #
        pg.init()
        self.screen = pg.display.set_mode(self.geometry)
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.board = Board()

        self.start_page = StartPage(self.screen, self.board)
        self.grid_page = GridPage(self.screen, self.board)
        self.instructions_page = InstructionsPage(self.screen)
        self.pages = [self.start_page, self.grid_page, self.instructions_page]
        self.current_page_idx = 0

        self.update()

    def update(self):
        current_page = self.pages[self.current_page_idx]
        page_idx = current_page.update()
        if page_idx == self.current_page_idx:
            self.clock.tick(10)
            self.update()
        else:
            self.set_screen(page_idx)

    def set_screen(self, page_idx):
        self.current_page_idx = page_idx
        self.update()