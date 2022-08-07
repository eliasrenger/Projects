# External imports
import pygame as pg
from sys import exit

# Internal imports
from src.config import *

"""
Ändra muspekaren till ett streck som det gör när det går att skriva.
"""

class StartPage():
    """Class StartPage defines the startpage."""
    def __init__(self, screen, board):
        """hmm"""
        self.screen = screen
        self.board = board
        self.width = RES[0]
        self.height = RES[1]
        self.img = 0
        self.texts = {}
        self.rectangles = {}

        # fonts
        self.std_font = pg.font.Font(None, 30)
        self.title_font = pg.font.Font(None, 50)
        self.fonts = {"std_font" : self.std_font,
                      "title_font" : self.title_font
                      }

        # colors
        self.background_clr = (240, 240, 245)
        self.selected_button_clr = (170, 170, 170)

        # background
        self.background = pg.Surface((self.width, self.height))
        self.background.fill(self.background_clr)

        # fonts
        self.std_font = pg.font.Font(None, 30)
        self.title_font = pg.font.Font(None, 50)
        self.fonts = {"std_font" : self.std_font,
                        "title_font": self.title_font}

        # text
        self.title = APP_TITLE
        self.create_text("title", "title_font", self.title, "center", (int(0.5 * self.width), int(0.15 * self.height)))
        self.create_text("instructions_text", "std_font", "Define the size of the plane.", "center", (int(0.5 * self.width), int(0.25 * self.height)))
        self.create_text("board_width_text", "std_font", "Enter the number of squares wide: ", "midleft", (int(0.1 * self.width), int(0.4 * self.height)))
        self.create_text("board_height_text", "std_font", "Enter the number of squares high: ", "midleft", (int(0.1 * self.width), int(0.6 * self.height)))
        self.create_text("create_plane", "std_font", "Create plane", "center", (int(0.8 * self.width), int(0.8 * self.height)))
        self.create_plane_surf, self.create_plane_rect = self.create_rect("create_plane", 130, 40, "center", (int(0.8 * self.width), int(0.8 * self.height)), False)

        self.create_rect("board_width_field", 100, 25, "midright", (int(0.9 * self.width), int(0.4 * self.height)))
        self.board_width_field_selected = False
        self.board_width_number = ""
        self.board_width_text = ""

        self.create_rect("board_height_field", 100, 25, "midright", (int(0.9 * self.width), int(0.6 * self.height)))
        self.board_height_field_selected = False
        self.board_height_number = ""
        self.board_height_text = ""

        self.rectangles_lst = list(self.rectangles.items())
        self.texts_lst = list(self.texts.items())

    def update(self):
        """Updates a frame and handles user input."""
        # user input
        self.img += 1
        if self.img % 10 == 1:
            self.img = 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.texts["create_plane"][1].collidepoint(event.pos) and event.button == 1:
                    if len(self.board_width_number) and len(self.board_height_number):
                        board_width, board_height = int(self.board_width_number), int(self.board_height_number)
                        if 1< board_width < 31 and 1 < board_height < 31:
                            self.board.set_geometry(board_width, board_height)
                            self.board_width_number, self.board_height_number = "", ""
                            self.board_width_field_selected, self.board_height_field_selected = False, False
                            return 1
                        else:
                            self.board_width_number, self.board_height_number = "",""
                            self.board_width_field_selected, self.board_height_field_selected = False, False
                elif self.rectangles["board_width_field"][1].collidepoint(event.pos) and event.button == 1:
                    self.board_width_field_selected, self.board_height_field_selected = True, False
                    self.img = 5
                elif self.rectangles["board_height_field"][1].collidepoint(event.pos) and event.button == 1:
                    self.board_width_field_selected, self.board_height_field_selected = False, True
                    self.img = 5
                elif self.board_width_field_selected or self.board_height_field_selected:
                    self.board_width_field_selected, self.board_height_field_selected = False, False
            if event.type == pg.KEYDOWN:
                key = ""
                if 48 <= event.key <= 57:
                    key = str(event.key - 48)  #converts key index to number
                if event.key == pg.K_BACKSPACE:
                    key = False
                if self.board_width_field_selected:
                    if type(key) == str:
                        self.board_width_number += key
                    else:
                        self.board_width_number = self.board_width_number[:-1]
                elif self.board_height_field_selected:
                    if type(key) == str:
                        self.board_height_number += key
                    else:
                        self.board_height_number = self.board_height_number[:-1]

        # puts surfaces on screen
        self.screen.blit(self.background, (0, 0))

        if self.create_plane_rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(self.screen, self.selected_button_clr, self.create_plane_rect)

        for text in self.texts_lst:
            self.screen.blit(text[1][0], text[1][1])

        for rectangle in self.rectangles_lst:
            pg.draw.rect(self.screen, "White", rectangle[1][1])


        if self.board_width_field_selected:
            if int(0.2 * self.img):
                self.board_width_text = f"{self.board_width_number}|"
            else:
                self.board_width_text = f"{self.board_width_number} "
        else:
            self.board_width_text = f"{self.board_width_number} "

        if self.board_height_field_selected:
            if int(0.2 * self.img):
                self.board_height_text = f"{self.board_height_number}|"
            else:
                self.board_height_text = f"{self.board_height_number} "
        else:
            self.board_height_text = f"{self.board_height_number} "

        height_surf, height_rect = self.create_text("height_input", "std_font", self.board_height_text, "midright", (int(0.9 * self.width) - 8, int(0.6 * self.height)), False)
        width_surf, width_rect = self.create_text("width_input", "std_font", self.board_width_text, "midright", (int(0.9 * self.width) - 8, int(0.4 * self.height)), False)
        self.screen.blit(width_surf, width_rect)
        self.screen.blit(height_surf, height_rect)

        pg.display.update()
        return 0

    def create_text(self, reference_name, font, text, point, position, add_to_dict = True):
        font = self.fonts[font]
        text_surf = font.render(text, True, "Black")
        text_rect = text_surf.get_rect()
        if point == "center":
            text_rect.center = position
        elif point == "midright":
            text_rect.midright = position
        elif point == "midleft":
            text_rect.midleft = position
        if add_to_dict:
            self.texts[reference_name] = (text_surf, text_rect)
        else:
            return text_surf, text_rect

    def create_rect(self, reference_name, width, height, point, position, add_to_dict = True):
        surface = pg.Surface((width, height))
        surf, rect = surface, surface.get_rect()
        if point == "center":
            rect.center = position
        elif point == "midright":
            rect.midright = position
        elif point == "midleft":
            rect.midleft = position
        if add_to_dict:
            self.rectangles[reference_name] = (surf, rect)
        else:
            return surf, rect