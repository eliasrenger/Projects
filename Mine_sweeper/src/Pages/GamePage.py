# External imports
import pygame as pg
from sys import exit

# Internal imports
from Mine_sweeper.src.config import *
from Mine_sweeper.src.game_logic import *
from Packages.pg_gui_framework import *

class GamePage:

    def __init__(self, screen, board):

        # Window dimensions
        self.res = RES
        self.menu_height = MENU_HEIGHT
        self.marginal_width = MARGINAL_WIDTH
        self.grid_marginal = GRID_MARGINAL
        self.cell_length = CELL_LENGTH
        self.top_right_board_cord = (MENU_HEIGHT + self.grid_marginal, MARGINAL_WIDTH + self.grid_marginal)


        # Define objects
        self.screen = screen
        self.board = board
        self.board.set_up_board(BOARD_WIDTH, BOARD_HEIGHT)
        self.board.set_difficulity(10)

        # Colors
        self.light_background_clr = LIGHT_BACKGROUND_CLR
        self.background_clr = BACKGROUND_CLR
        self.dark_background_clr = DARK_BACKGROUND_CLR

        # Surfaces
        self.background_surf = pg.Surface(self.res)
        self.background_surf.fill(self.background_clr)

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

        # display
        mouse_pos = pg.mouse.get_pos()
        self.screen.blit(self.background_surf, (0,0))

        for text in self.texts:
            text.display_text()

        for button in self.buttons:
            button.display_button(mouse_pos)

        return 1

    def cell_to_screen(self, cell_cord):
        x, y = cell_cord
        screen_cord = (int(self.marginal_width + x * (self.grid_marginal + self.cell_length)),
                       int(self.menu_height + y * (self.grid_marginal + self.cell_length)))
        return screen_cord

    def screen_to_cell(self, screen_cord):
        x, y = screen_cord
        cell_cord = (int((x - self.marginal_width)/((self.grid_marginal + self.cell_length))),
                     int((y - self.menu_height)/((self.grid_marginal + self.cell_length))))
        return cell_cord

