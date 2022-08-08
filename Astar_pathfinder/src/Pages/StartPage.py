# External imports
import pygame as pg
from sys import exit

# Internal imports
from src.config import *
from src.pg_buttons_texts import *

"""
Ändra muspekaren till ett streck som det gör när det går att skriva.
"""

class StartPage():
    """Class StartPage defines the startpage."""
    def __init__(self, screen, board):
        """hmm"""
        self.screen = screen
        self.board = board
        self.width, self.height = RES
        self.img = 0
        self.texts = []
        self.buttons = []

        # fonts
        self.std_font = pg.font.Font(None, 30)
        self.title_font = pg.font.Font(None, 50)

        # colors
        self.background_clr = (240, 240, 245)
        self.hovered_button_clr = (170, 170, 170)

        # background
        self.background = pg.Surface((self.width, self.height))
        self.background.fill(self.background_clr)

        # text
        self.title = APP_TITLE
        self.texts.append(Text(self.screen, self.title_font, "center", (int(0.5 * self.width), int(0.15 * self.height)),
                               self.title))
        self.texts.append(Text(self.screen, self.std_font, "center", (int(0.5 * self.width), int(0.25 * self.height)),
                               "Define the size of the plane"))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.4 * self.height)),
                                "Enter the number of squares wide"))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.6 * self.height)),
                               "Enter the number of squares high"))
        self.width_field_selected = Text(self.screen, self.std_font, "midleft", (int(0.9 * self.width) - 10, int(0.4 * self.height)), "|")
        self.height_field_selected = Text(self.screen, self.std_font, "midleft", (int(0.9 * self.width) - 10, int(0.6 * self.height)), "|")

        # buttons
        self.buttons.append(Button(self.screen, self.std_font, "center", (int(0.8 * self.width), int(0.8 * self.height)),
                                   (130,40), self.background_clr, "Create plane", self.hovered_button_clr))
        self.buttons.append(Button(self.screen, self.std_font, "midright", (int(0.9 * self.width) - 10, int(0.4 * self.height)), (100, 25),
                                   "White", "", "White", (int(0.9 * self.width), int(0.4 * self.height)), "midright"))
        self.buttons.append(Button(self.screen, self.std_font, "midright", (int(0.9 * self.width) - 10, int(0.6 * self.height)), (100, 25),
                                    "White", "", "White", (int(0.9 * self.width), int(0.6 * self.height)), "midright"))

    def update(self):
        """Updates a frame and handles user input."""
        # drives the blinking animation when field is selected
        self.img = (self.img + 1) % 16

        # user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            # create_plane button logic
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.buttons[0].back_rect.collidepoint(event.pos):
                    if len(self.buttons[1].text) and len(self.buttons[2].text):
                        board_width, board_height = int(self.buttons[1].text), int(self.buttons[2].text)
                        for i in range(1, 3):
                            self.buttons[i].update_text("")
                            self.buttons[i].selected = False
                            in_width_limit = board_width in range(2, 31)
                            in_height_limit = board_height in range(2, 31)
                        if in_width_limit and in_height_limit:  # makes sure the board is a reasonable size
                            self.board.set_geometry(board_width, board_height)
                            return 1

                # sets selected button
                for i in range(1, 3):
                    if self.buttons[i].back_rect.collidepoint(event.pos):
                        self.buttons[i].selected = True
                        self.img = 5
                    else:
                        self.buttons[i].selected = False
            # inputs in field
            if event.type == pg.KEYDOWN:
                for button in self.buttons:
                    if button.selected:
                        break
                else:
                    continue
                if 48 <= event.key <= 57:
                    key = str(event.key - 48)  #converts key index to number
                    new_text = button.text + key
                elif event.key == pg.K_BACKSPACE:
                    new_text = button.text[:-1]
                else:
                    continue
                button.update_text(new_text)

        # puts surfaces on screen
        self.screen.blit(self.background, (0, 0))

        mouse_pos = pg.mouse.get_pos()
        for text in self.texts:
            text.display_text()

        for button in self.buttons:
            button.display_button(mouse_pos)

        # blinking animation
        if self.img >= 8:
            if self.buttons[1].selected:
                self.width_field_selected.display_text()
            elif self.buttons[2].selected:
                self.height_field_selected.display_text()

        pg.display.update()
        return 0