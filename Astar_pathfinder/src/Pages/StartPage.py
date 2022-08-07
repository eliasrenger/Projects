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
        self.img = 0

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
        self.set_board_width_text_surf = self.font.render("Enter number of squares in the horizontal direction:", True, "Black")
        self.set_board_width_text_rect = self.set_board_width_text_surf.get_rect(
            midleft=(int(0.1 * self.width), int(0.4 * self.height)))

        self.board_width_field_rect = pg.Surface((80, 25))
        self.board_width_field_rect.fill("White")
        self.board_width_field_rect = self.board_width_field_rect.get_rect(midright=(int(0.9 * self.width), int(0.4 * self.height)))
        self.board_width_field_selected = False
        self.board_width_number = ""
        self.board_width_text = ""

        #self.set_height_surf = pg.Surface()
        #self.set_height_surf.fill("White")
        self.set_height_text_surf = self.font.render("Enter number of squares in the vertical direction:", True, "Black")
        self.set_height_text_rect = self.set_height_text_surf.get_rect(
            midleft=(int(0.1 * self.width), int(0.6 * self.height)))

        self.board_height_field_rect = pg.Surface((80, 25))
        self.board_height_field_rect.fill("White")
        self.board_height_field_rect = self.board_height_field_rect.get_rect(midright=(int(0.9 * self.width), int(0.6 * self.height)))
        self.board_height_field_selected = False
        self.board_height_number = ""
        self.board_height_text = ""

        # create plane button
        #self.create_plane_surf = pg.Surface()
        #self.create_plane_surf.fill("White")
        self.create_plane_text_surf = self.font.render("Create plane", True, "Black")
        self.create_plane_text_rect = self.create_plane_text_surf.get_rect(
            center = (int(0.7 * self.width), int(0.8 * self.height)))

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
                if self.create_plane_text_rect.collidepoint(event.pos) and event.button == 1:
                    if len(self.board_width_number) and len(self.board_height_number):
                        board_width, board_height = int(self.board_width_number), int(self.board_height_number)
                        if board_width < 31 and board_height < 31:
                            self.board.set_geometry(board_width, board_height)
                            self.board_width_number, self.board_height_number = "", ""
                            self.board_width_field_selected, self.board_height_field_selected = False, False
                            return 1
                        else:
                            self.board_width_number, self.board_height_number = "",""
                            self.board_width_field_selected, self.board_height_field_selected = False, False

                elif self.board_width_field_rect.collidepoint(event.pos) and event.button == 1:
                    self.board_width_field_selected, self.board_height_field_selected = True, False
                    self.img = 5
                elif self.board_height_field_rect.collidepoint(event.pos) and event.button == 1:
                    self.board_width_field_selected, self.board_height_field_selected = False, True
                    self.img = 5
                elif self.board_width_field_selected or self.board_height_field_selected:
                    self.board_width_field_selected, self.board_height_field_selected = False, False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    key = False
                elif event.key == pg.K_0:
                    key = "0"
                elif event.key == pg.K_1:
                    key = "1"
                elif event.key == pg.K_2:
                    key = "2"
                elif event.key == pg.K_3:
                    key = "3"
                elif event.key == pg.K_4:
                    key = "4"
                elif event.key == pg.K_5:
                    key = "5"
                elif event.key == pg.K_6:
                    key = "6"
                elif event.key == pg.K_7:
                    key = "7"
                elif event.key == pg.K_8:
                    key = "8"
                elif event.key == pg.K_9:
                    key = "9"
                if self.board_width_field_selected:
                    if key:
                        self.board_width_number += key
                    else:
                        self.board_width_number = self.board_width_number[:-1]
                elif self.board_height_field_selected:
                    if key:
                        self.board_height_number += key
                    else:
                        self.board_height_number = self.board_height_number[:-1]


        # puts surfaces on screen
        self.screen.blit(self.background, (0, 0))

        pg.draw.rect(self.screen, "White", self.title_text_rect)
        self.screen.blit(self.title_text_surf, self.title_text_rect)

        pg.draw.rect(self.screen, "White", self.instructions_text_rect)
        self.screen.blit(self.instructions_text_surf, self.instructions_text_rect)

        pg.draw.rect(self.screen, "White", self.set_board_width_text_rect)
        self.screen.blit(self.set_board_width_text_surf, self.set_board_width_text_rect)

        pg.draw.rect(self.screen, "White", self.set_height_text_rect)
        self.screen.blit(self.set_height_text_surf, self.set_height_text_rect)

        pg.draw.rect(self.screen, "White", self.create_plane_text_rect)
        self.screen.blit(self.create_plane_text_surf, self.create_plane_text_rect)

        pg.draw.rect(self.screen, "White", self.board_width_field_rect)
        pg.draw.rect(self.screen, "White", self.board_height_field_rect)


        if self.board_width_field_selected:
            if int(0.2 * self.img):
                self.board_width_text = f"{self.board_width_number}|"
            else:
                self.board_width_text = f"{self.board_width_number} "
        else:
            self.board_width_text = f"{self.board_width_number} "
        self.board_width_text_surf = self.font.render(self.board_width_text, True, "Black")
        self.board_width_text_rect = self.board_width_text_surf.get_rect(midright=((int(0.9 * self.width) - 8, int(0.4 * self.height))))
        self.screen.blit(self.board_width_text_surf, self.board_width_text_rect)

        if self.board_height_field_selected:
            if int(0.2 * self.img):
                self.board_height_text = f"{self.board_height_number}|"
            else:
                self.board_height_text = f"{self.board_height_number} "
        else:
            self.board_height_text = f"{self.board_height_number} "
        self.board_height_text_surf = self.font.render(self.board_height_text, True, "Black")
        self.board_height_text_rect = self.board_height_text_surf.get_rect(
            midright=((int(0.9 * self.width) - 8, int(0.6 * self.height))))
        self.screen.blit(self.board_height_text_surf, self.board_height_text_rect)

        pg.display.update()
        return 0