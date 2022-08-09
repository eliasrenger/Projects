# External imports
import pygame as pg
from sys import exit

# Internal imports
from src.Astar_algorithm import *
from src.config import *
from src.gui_framework import *


class GridPage():
    """GridPage class defines the grid page"""
    def __init__(self, screen, board):
        """"""
        # objects
        self.screen = screen
        self.board = board

        # scales parts of the screen
        self.width, self.height = RES
        self.menu_width = 0.3 * self.width
        self.menu_center = int(self.menu_width / 2)
        self.button_height = int(0.9 * self.height / 8)
        self.button_marginal_height = int(0.06 * self.height / 8)
        self.button_width = int(0.94 * self.menu_width)
        self.button_marginal_width = int(0.03 * self.menu_width)

        # colors
        self.button_clr = (250, 250, 250)
        self.hovered_button_clr = (190, 190, 190)

        # background and standard font
        self.background = pg.Surface((self.width, self.height))
        self.background.fill("Black")
        self.font = pg.font.Font(None, int(0.08 * self.height))

        # defines states of the grid
        self.running = False
        self.cleared = True

        # types of squares on the grid
        self.neutral_squares = []
        self.obstacles = []
        self.start_goal_squares = [None, None]

        # lists of squares affected by pathfinder
        self.visited_sq = []
        self.path = []
        self.showed_visited_sq = []
        self.showed_path = []

        # lists of buttons and surfaces
        self.buttons = []

        # run button
        self.run_button = Button(self.screen, self.font, "center",
                                 (self.menu_center, int(self.button_marginal_height + 0.5 * self.button_height)),
                                 (self.button_width, self.button_height), self.button_clr, "RUN", self.hovered_button_clr)
        self.buttons.append(self.run_button)

        # pause button
        self.pause_button = Button(self.screen, self.font, "center",
                                 (self.menu_center, int(2 * self.button_marginal_height + 1.5 * self.button_height)),
                                 (self.button_width, self.button_height), self.button_clr, "PAUSE", self.hovered_button_clr)
        self.buttons.append(self.pause_button)

        # clear button
        self.clear_button = Button(self.screen, self.font, "center",
                                 (self.menu_center, int(3 * self.button_marginal_height + 2.5 * self.button_height)),
                                 (self.button_width, self.button_height), self.button_clr, "CLEAR", self.hovered_button_clr)
        self.buttons.append(self.clear_button)

        # reset button
        self.reset_button = Button(self.screen, self.font, "center",
                                   (self.menu_center, int(4 * self.button_marginal_height + 3.5 * self.button_height)),
                                   (self.button_width, self.button_height), self.button_clr, "RESET",
                                   self.hovered_button_clr)
        self.buttons.append(self.reset_button)

        # randomize button
        self.randomize_button = Button(self.screen, self.font, "center",
                                 (self.menu_center, int(5 * self.button_marginal_height + 4.5 * self.button_height)),
                                 (self.button_width, self.button_height), self.button_clr, "RANDOMIZE", self.hovered_button_clr)
        self.buttons.append(self.randomize_button)

        # back button
        self.back_button = Button(self.screen, self.font, "center",
                                 (self.menu_center, int(6 * self.button_marginal_height + 5.5 * self.button_height)),
                                 (self.button_width, self.button_height), self.button_clr, "BACK", self.hovered_button_clr)
        self.buttons.append(self.back_button)

        # instructions button
        self.instructions_button = Button(self.screen, self.font, "center",
                                 (self.menu_center, int(7 * self.button_marginal_height + 6.5 * self.button_height)),
                                 (self.button_width, self.button_height), self.button_clr, "INSTRUCTIONS", self.hovered_button_clr)
        self.buttons.append(self.instructions_button)


    def set_up_grid(self):
        """Defines the grid shown to user from geometry of the board."""
        self.nr_sq_x, self.nr_sq_y = self.board.width, self.board.height
        if (self.width - self.menu_width) / self.nr_sq_x < self.height / self.nr_sq_y:
            self.grid_marginal = int(0.05 * (self.width - self.menu_width) / (self.nr_sq_x + 1))
            self.sq_length = int(0.95 * (self.width - self.menu_width) / self.nr_sq_x)
        else:
            self.grid_marginal = int(0.05 * self.height / (self.nr_sq_y + 1))
            self.sq_length = int(0.95 * self.height / self.nr_sq_y)

        # surfaces for squares
        self.start_surf = pg.Surface((self.sq_length, self.sq_length))
        self.goal_surf = pg.Surface((self.sq_length, self.sq_length))
        self.path_surf = pg.Surface((self.sq_length, self.sq_length))
        self.obstacle_surf = pg.Surface((self.sq_length, self.sq_length))
        self.neutral_surf = pg.Surface((self.sq_length, self.sq_length))
        self.visited_surf = pg.Surface((self.sq_length, self.sq_length))
        self.start_surf.fill("#B5FAD6")
        self.goal_surf.fill("#FFB1A1")
        self.path_surf.fill("#9AB7D3")
        self.obstacle_surf.fill("Grey")
        self.neutral_surf.fill("White")
        self.visited_surf.fill("#DDF2FD")

        # creates grid of neutral squares
        neutral_squares = []
        for i in range(self.nr_sq_x):
            for j in range(self.nr_sq_y):
                neutral_squares.append((i + 1, j + 1))
        self.neutral_squares = self.squares_to_screen_coordinates(neutral_squares)

        # grid defined for board geometry is complete
        self.board.geometry_changed = False

    def set_up_squares(self):
        """Creates lists of special squares on the board and their coordinates on the screen."""
        self.obstacles = self.squares_to_screen_coordinates(self.board.obstacles)
        self.start_goal_squares = self.squares_to_screen_coordinates([self.board.start, self.board.goal])
        self.board.squares_changed = False

    def find_path(self):
        """Finds path and converts affected squares on board to coordinate on screen."""
        self.path, self.visited_sq = self.board.pathfinder()
        self.visited_sq = self.squares_to_screen_coordinates(self.visited_sq)
        if self.path:
            self.path = self.squares_to_screen_coordinates(self.path)

    def run(self):
        """Begins visualization of path."""
        if self.board.start and self.board.goal:
            self.running = True
            self.cleared = False

    def pause(self):
        """Pauses visualization of path."""
        self.running = False

    def clear(self):
        """Removes shown path."""
        self.showed_path = []
        self.showed_visited_sq = []
        self.running = False
        self.cleared = True

    def randomize(self):
        self.path = None
        if not (self.board.start and self.board.goal):
            self.board.randomize_start_goal()
        self.clear()
        while not self.path:
            self.board.randomize_obstacles()
            self.find_path()
        self.set_up_grid()

    def reset_board(self):
        self.clear()
        self.board.obstacles = []
        self.board.set_start(None)
        self.board.set_goal(None)

    def update(self):
        """Updates a frame and handles user input."""
        # setting up grid after geometry is set
        if self.board.geometry_changed:
            self.set_up_grid()

        # user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # shows path for user
                    if self.run_button.back_rect.collidepoint(event.pos):
                        self.run()
                    # pause path visualization
                    elif self.pause_button.back_rect.collidepoint(event.pos):
                        self.pause()
                    # clears shown path
                    elif self.clear_button.back_rect.collidepoint(event.pos):
                        self.clear()
                    elif self.reset_button.back_rect.collidepoint(event.pos):
                        self.reset_board()
                    # randomize obstacles on board
                    elif self.randomize_button.back_rect.collidepoint(event.pos):
                        self.randomize()
                    # user returns to StartPage
                    elif self.back_button.back_rect.collidepoint(event.pos):
                        self.reset_board()
                        return 0
                    # user opens InstructionsPage
                    elif self.instructions_button.back_rect.collidepoint(event.pos):
                        self.clear()
                        return 2
                    elif self.cleared:
                        # user manipulation of obstacles
                        selected_square = self.screen_coordinate_to_square(event.pos)
                        if selected_square in self.board.obstacles:
                            self.board.remove_obstacle(selected_square)
                        elif not selected_square in [self.board.start, self.board.goal]:
                            self.board.add_obstacle(selected_square)
                # user manipulation of start and goal
                elif event.button == 3 and self.cleared:
                    selected_square = self.screen_coordinate_to_square(event.pos)
                    if selected_square == self.board.start:
                        self.board.set_start(None)
                    elif selected_square == self.board.goal:
                        self.board.set_goal(None)
                    elif not self.board.start:
                        self.board.set_start(selected_square)
                    elif not self.board.goal:
                        self.board.set_goal(selected_square)

        # finds new path after changes
        if self.board.squares_changed:
            self.set_up_squares()
            self.find_path()

        # adds background
        self.screen.blit(self.background, (0, 0))

        # display buttons
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.display_button(mouse_pos)

        # effect of "movement" by adding one square per frame
        if self.running:
            if not self.showed_visited_sq == self.visited_sq:
                idx = len(self.showed_visited_sq)
                self.showed_visited_sq.append(self.visited_sq[idx])
            elif not self.showed_path == self.path and self.path:
                idx = len(self.showed_path)
                self.showed_path.append(self.path[idx])

        # adds the grid to the screen
        for square in self.neutral_squares:
            self.screen.blit(self.neutral_surf, square)

        for obstacle in self.obstacles:
            self.screen.blit(self.obstacle_surf, obstacle)

        for step in self.showed_visited_sq:
            self.screen.blit(self.visited_surf, step)

        for step in self.showed_path:
            self.screen.blit(self.path_surf, step)

        if self.start_goal_squares[0]:
            self.screen.blit(self.start_surf, self.start_goal_squares[0])
        if self.start_goal_squares[1]:
            self.screen.blit(self.goal_surf, self.start_goal_squares[1])

        pg.display.update()
        return 1

    def squares_to_screen_coordinates(self, cords):
        """Converts squares on the board to a coordinates (topleft of surface) on the screen"""
        new_cords = []
        for cord in cords:
            if cord:
                new_x = int(self.menu_width + self.grid_marginal + (cord[0] - 1) * (self.sq_length + self.grid_marginal))
                new_y = int(self.grid_marginal + (cord[1] - 1) * (self.sq_length + self.grid_marginal))
                new_cords.append((new_x, new_y))
            else:
                new_cords.append(None)  # undersök om detta behövs och vad det leder till om det inträffar
        return new_cords

    def screen_coordinate_to_square(self, cord):
        """Converts coordinate on screen to a square on the board."""
        new_x = int((cord[0] - self.menu_width + self.sq_length) / (self.sq_length + self.grid_marginal))
        new_y = int((cord[1]  + self.sq_length) / (self.sq_length + self.grid_marginal))
        return (new_x, new_y)