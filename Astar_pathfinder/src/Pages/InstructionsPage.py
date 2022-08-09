# External imports
import pygame as pg
from sys import exit

# Internal imports
from src.config import *
from src.gui_framework import *

class InstructionsPage():

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = RES

        # colors
        self.background_clr = (240, 240, 245)
        self.hovered_button_clr = (170, 170, 170)

        # fonts
        self.std_font = pg.font.Font(None, 30)
        self.title_font = pg.font.Font(None, 50)

        # background
        self.background_surf = pg.Surface((self.width, self.height))
        self.background_surf.fill(self.background_clr)

        # texts
        self.texts = []
        self.texts.append(Text(self.screen, self.title_font, "center", (int(0.5 * self.width), int(0.1 * self.height)),
                               "Instructions"))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.2 * self.height)),
                               "White squares are walkable and grey squares are obstacles."))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.25 * self.height)),
                               "Press left click to turn a walkable-square to an obstacle-square or the other way around."))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.3 * self.height)),
                               "Green square is the start-square and red square is the goal-square."))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.35 * self.height)),
                               "Press right click on a walkable-square to turn it to a start-square"))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.4 * self.height)),
                               "or goal-square or the other way around"))
        self.texts.append(Text(self.screen, self.std_font, "midleft", (int(0.1 * self.width), int(0.5 * self.height)),
                               "To make changes to the board it must first be cleared."))


        # buttons
        self.buttons = []
        self.back_to_grid_button = Button(self.screen, self.std_font, "center", (int(0.75 * self.width), int(0.8 * self.height)),
                                   (120, 40), self.background_clr, "Back to grid", self.hovered_button_clr)
        self.buttons.append(self.back_to_grid_button)

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.back_to_grid_button.back_rect.collidepoint(event.pos):
                    return 1

        self.screen.blit(self.background_surf, (0, 0))

        for text in self.texts:
            text.display_text()

        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.display_button(mouse_pos)

        pg.display.update()
        return 2