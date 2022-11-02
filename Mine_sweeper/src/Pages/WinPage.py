# External imports
import pygame as pg
from sys import exit

# Internal imports

class WinPage:

    def __init__(self):
        pass

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
        return 3