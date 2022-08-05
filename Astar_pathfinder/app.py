#Exetutable

#Internal imports
from src.gui import GUI
from src.config import *

class App():

    def __init__(self):
        self.gui = GUI()

    def start(self):
        self.gui.update()

if __name__ == "__main__":
    app = App()
    app.start()