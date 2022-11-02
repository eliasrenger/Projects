# External imports
import pygame as pg

# Internal imports
from Mine_sweeper.src.config import *
from Mine_sweeper.src.game_logic import *
from Mine_sweeper.src.Pages.StartPage import StartPage
from Mine_sweeper.src.Pages.GamePage import GamePage
from Mine_sweeper.src.Pages.MenuPage import MenuPage
from Mine_sweeper.src.Pages.WinPage import WinPage
from Mine_sweeper.src.Pages.LosePage import LosePage

class GUI:

    def __init__(self):
        self.title = "Mine Sweeeper"
        self.geometry = RES

        pg.init()
        self.screen = pg.display.set_mode(self.geometry)
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.fps = 16

        self.board = Board()
        self.start_page = StartPage(self.screen, self.board)
        self.game_page = GamePage(self.screen, self.board)
        self.menu_page = MenuPage(self.screen, self.board)
        self.win_page = WinPage(self.screen)
        self.lose_page = LosePage(self.screen)

        self.pages = [self.start_page, self.game_page, self.menu_page, self.win_page, self.lose_page]
        self.cur_page_idx = 0

    def update(self):
        cur_page = self.pages[self.cur_page_idx]
        page_idx = cur_page.update()
        self.click.tick(self.fps)
        if page_idx == self.cur_page_idx:
            self.clock.tick(self.fps)
        else:
            self.set_page(page_idx)

    def set_page(self, page_idx):
        self.cur_page_idx = page_idx
