# External imports
import pygame as pg
from sys import exit

# Internal imports
from src.config import *

class StartPage():
    """Class StartPage defines the startpage."""
    def __init__(self, screen, board):
        """hmm"""
        self.screen = screen
        self.board = board
        self.width = RES[0]
        self.height = RES[1]

        # background
        self.background = pg.Surface((self.width, self.height))
        self.background.fill("Black")

        # fonts
        self.font = pg.font.Font(None, 30)
        self.title_font = pg.font.Font(None, 50)

        # text
        self.title = APP_TITLE
        #self.title_surf = pg.Surface()
        #self.title_surf.fill("White")
        self.title_text_surf = self.title_font.render(f"{self.title}", True, "Black")
        self.title_text_rect = self.title_text_surf.get_rect(
            center = (int(0.5 * self.width), int(0.15 * self.height)))

        #self.instructions_surf = pg.Surface(())
        #self.instructions_surf.fill("White")
        self.instructions_text_surf = self.font.render("Define the plane on which the labyrinth is being built.", True, "Black")
        self.instructions_text_rect = self.instructions_text_surf.get_rect(center = (int(0.5 * self.width), int(0.3 * self.height)))

        #self.set_width_surf = pg.Surface()
        #self.set_width_surf.fill("White")
        self.set_width_text_surf = self.font.render("Enter number of squares in the horizontal direction:", True, "Black")
        self.set_width_text_rect = self.set_width_text_surf.get_rect(
            midleft=(int(0.1 * self.width), int(0.4 * self.height)))

        #self.set_height_surf = pg.Surface()
        #self.set_height_surf.fill("White")
        self.set_height_text_surf = self.font.render("Enter number of squares in the vertical direction:", True, "Black")
        self.set_height_text_rect = self.set_height_text_surf.get_rect(
            midleft=(int(0.1 * self.width), int(0.6 * self.height)))

        # create plane button
        #self.create_plane_surf = pg.Surface()
        #self.create_plane_surf.fill("White")
        self.create_plane_text_surf = self.font.render("Create plane", True, "Black")
        self.create_plane_text_rect = self.create_plane_text_surf.get_rect(
            center = (int(0.7 * self.width), int(0.8 * self.height)))

    def update(self):
        """Updates a frame and handles user input."""
        # user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.create_plane_text_rect.collidepoint(event.pos) and event.button == 1:
                    # predefined geometry
                    self.board.set_geometry(10, 10)
                    return 1

        # puts surfaces on screen
        self.screen.blit(self.background, (0, 0))

        pg.draw.rect(self.screen, "White", self.title_text_rect)
        self.screen.blit(self.title_text_surf, self.title_text_rect)

        pg.draw.rect(self.screen, "White", self.instructions_text_rect)
        self.screen.blit(self.instructions_text_surf, self.instructions_text_rect)

        pg.draw.rect(self.screen, "White", self.set_width_text_rect)
        self.screen.blit(self.set_width_text_surf, self.set_width_text_rect)

        pg.draw.rect(self.screen, "White", self.set_height_text_rect)
        self.screen.blit(self.set_height_text_surf, self.set_height_text_rect)

        pg.draw.rect(self.screen, "White", self.create_plane_text_rect)
        self.screen.blit(self.create_plane_text_surf, self.create_plane_text_rect)

        pg.display.update()
        return 0