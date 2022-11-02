# External imports


# Internal imports
from src.gui import *

class App:

    def __init__(self):
        self.gui = GUI()

    def run(self):
        self.gui.update()

if __name__ == "__main__":
    app = App()
    app.run