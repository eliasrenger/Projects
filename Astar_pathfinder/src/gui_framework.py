# External imports
import pygame as pg

"""
add class textbox
add action function for buttons
"""

class Text():

    def __init__(self, screen, font, text_point, text_pos, text = "", text_clr = (0, 0, 0)):
        self.screen = screen
        self.text = text
        self.font = font
        self.text_clr = text_clr
        self.text_surf = self.font.render(self.text, True, self.text_clr)
        self.text_rect = self.text_surf.get_rect()
        self.place(self.text_rect, text_point, text_pos)

    def display_text(self):
        self.screen.blit(self.text_surf, self.text_rect)

    def place(self, rectangle, point, position):
        if point == "center":
            rectangle.center = position
        elif point == "topleft":
            rectangle.topleft = position
        elif point == "topright":
            rectangle.topright = position
        elif point == "midright":
            rectangle.midright = position
        elif point == "midleft":
            rectangle.midleft = position


class Button(Text):

    def __init__(self, screen, font, text_point, text_pos, size, back_clr = None, text = "",
                 back_clr_hovered = None, back_pos = None, back_point = None, text_clr = (0, 0, 0)):
        super().__init__(screen, font, text_point, text_pos, text, text_clr)

        self.text_point = text_point
        self.text_pos = text_pos

        if not back_pos:
            back_pos = text_pos
            back_point = text_point
        self.back_surf = pg.Surface(size)
        self.back_rect = self.back_surf.get_rect()
        self.back_clr = back_clr
        self.back_clr_hovered = back_clr_hovered
        self.back_cur_clr = self.back_clr
        self.place(self.back_rect, back_point, back_pos)

        self.selected = False

    def display_button(self, mousepos = False):
        self.hovered(mousepos)
        pg.draw.rect(self.screen, self.back_cur_clr, self.back_rect)
        self.screen.blit(self.text_surf, self.text_rect)

    def hovered(self, mousepos):
        if mousepos and self.back_rect.collidepoint(mousepos):
            self.back_cur_clr = self.back_clr_hovered
        else:
            self.back_cur_clr = self.back_clr

    def update_text(self, new_text):
        self.text = new_text
        self.text_surf = self.font.render(self.text, True, self.text_clr)
        self.text_rect = self.text_surf.get_rect()
        self.place(self.text_rect, self.text_point, self.text_pos)

    def change_state(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True


class Textbox(Button):

    def __init__(self, screen, font, text_point, text_pos, size, back_clr = None, text = "",
                 back_pos = None, back_point = None, back_clr_hovered = None, text_clr = (0, 0, 0)):
        super().__init__(screen, font, text_point, text_pos, size, back_clr, text,
                 back_clr_hovered, back_pos, back_point, text_clr)
        pass


    def animation(self):
        pass
