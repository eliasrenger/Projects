# External imports
import random as rn

# Internal imports

class Board:

    def __init__(self):
        self.width = None
        self.height = None
        self.mines = []
        self.cells = []
        self.cell_dict = {}
        self.weights = [1, 1]

        self.geometry_changed = False

    def set_up_board(self, width, height):
        self.width = width
        self.height = height
        self.geometry_changed = True
        valid_board = False

        while not valid_board:
            self.cells = []
            self.create_cells()
            valid_board = self.set_up_cells()

    def create_cells(self):
        for i in range(self.width):
            for j in range(self.height):
                is_mine = rn.choices([True, False], self.weights)
                cell = Cell((i, j), is_mine)
                if is_mine:
                    self.mines.append(cell)
                self.cells.append(cell)
                self.cell_dict[f"({i}, {j})"] = cell

    def set_up_cells(self):
        for mine in self.mines:
            cord = mine.get_pos
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if not k and not l:
                        continue
                    adj_cord = (cord[0] + k, cord[1] + l)
                    onboard = (0 < adj_cord[0] <= self.width and 0 < adj_cord[1] <= self.height)
                    if onboard:
                        cell = self.cell_dict[adj_cord]
                        cell.add_sur_mine()
                        if cell.get_num_sur_mines > 4:
                            return False
        return True

    def reset(self):
        self.width = None
        self.height = None
        self.mines = []
        self.cells = []
        self.cell_dict = {}
        self.weights = [1, 1]

        self.geometry_changed = False

    def set_difficulity(self, difficulity):
        self.weights = [1, difficulity]


class Cell:

    def __init__(self, coordinate, is_mine):
        self.coordinate = coordinate
        self.is_mine = is_mine
        self.opened = False
        self.flagged = False
        self.surrounding_mines = 0

    def add_sur_mine(self):
        self.surrounding_mines += 1

    def change_flagging(self):
        if self.flagged:
            self.flagged = False
        else:
            self.flagged = True

    def open(self):
        if not self.flagged:
            self.opened = True

    def get_pos(self):
        return self.coordinate

    def get_num_sur_mines(self):
        return self.surrounding_mines

    def get_state(self):
        return self.opened, self.flagged