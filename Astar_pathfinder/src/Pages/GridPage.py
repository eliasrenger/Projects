# External imports
import pygame as pg
from sys import exit

# Internal imports
from src.Astar_algorithm import *
from src.config import *

"""
---Anteckningar---
Koden kraschar om ingen väg finns mellan start och goal pga obstacles.
 - hantera returneningen path = False
"""

class GridPage():
    """GridPage class defines the grid page"""
    def __init__(self, screen, board):
        """"""
        # objects needed to
        self.screen = screen
        self.board = board

       # scales of parts of the screen
        self.width = RES[0]
        self.height = RES[1]
        self.menu_width = 0.3 * self.width
        self.menu_center = int(self.menu_width / 2)
        self.button_height = int(0.9 * self.height / 6)
        self.button_marginal_height = int(0.06 * self.height / 6)
        self.button_width = int(0.94 * self.menu_width)
        self.button_marginal_width = int(0.03 * self.menu_width)

        # background and standard font
        self.background = pg.Surface((self.width, self.height))
        self.background.fill("Black")
        self.font = pg.font.Font(None, int(0.08 * self.height))

        # run button
        self.run_button_surf = pg.Surface((self.button_width, self.button_height))
        self.run_button_surf.fill("White")
        self.run_button_rect = self.run_button_surf.get_rect(center=(self.menu_center, int(self.button_marginal_height + 0.5 * self.button_height)))
        self.run_text_surf = self.font.render("RUN", True, "Black")
        self.run_text_rect = self.run_text_surf.get_rect(
            center=(self.menu_center, int(1 * self.button_marginal_height + 0.5 * self.button_height)))

        # pause button
        self.pause_button_surf = pg.Surface((self.button_width, self.button_height))
        self.pause_button_surf.fill("White")
        self.pause_button_rect = self.pause_button_surf.get_rect(center=(self.menu_center, int(2 * self.button_marginal_height + 1.5 * self.button_height)))
        self.pause_text_surf = self.font.render("PAUSE", True, "Black")
        self.pause_text_rect = self.pause_text_surf.get_rect(
            center=(self.menu_center, int(2 * self.button_marginal_height + 1.5 * self.button_height)))

        # clear button
        self.clear_button_surf = pg.Surface((self.button_width, self.button_height))
        self.clear_button_surf.fill("White")
        self.clear_button_rect = self.clear_button_surf.get_rect( center=(self.menu_center, int(3 * self.button_marginal_height + 2.5 * self.button_height)))
        self.clear_text_surf = self.font.render("CLEAR", True, "Black")
        self.clear_text_rect = self.clear_text_surf.get_rect(
            center=(self.menu_center, int(3 * self.button_marginal_height + 2.5 * self.button_height)))

        # back button
        self.back_button_surf = pg.Surface((self.button_width, self.button_height))
        self.back_button_surf.fill("White")
        self.back_button_rect = self.back_button_surf.get_rect(center=(self.menu_center, int(4 * self.button_marginal_height + 3.5 * self.button_height)))
        self.back_text_surf = self.font.render("BACK", True, "Black")
        self.back_text_rect = self.back_text_surf.get_rect(
            center=(self.menu_center, int(4 * self.button_marginal_height + 3.5 * self.button_height)))

        # instructions button
        self.instructions_button_surf = pg.Surface((self.button_width, self.button_height))
        self.instructions_button_surf.fill("White")
        self.instructions_button_rect = self.instructions_button_surf.get_rect(center=(self.menu_center, int(5 * self.button_marginal_height + 4.5 * self.button_height)))
        self.instructions_text_surf = self.font.render("INSTRUCTIONS", True, "BLack")
        self.instructions_text_rect = self.instructions_text_surf.get_rect(center = (self.menu_center, int(5 * self.button_marginal_height + 4.5 * self.button_height)))

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

    def set_up_grid(self):
        """Defines the grid shown to user from geometry of the board."""
        self.nr_sq_x = self.board.width
        self.nr_sq_y = self.board.height
        self.grid_marginal_width = int(0.05 * (self.width - self.menu_width) / (self.nr_sq_x + 1))
        self.grid_marginal_height = int(0.05 * self.height / (self.nr_sq_y + 1))
        self.sq_width = int(0.95 * (self.width - self.menu_width) / self.nr_sq_x)
        self.sq_height = int(0.95 * self.height / self.nr_sq_y)

        # surfaces for squares
        self.start_surf = pg.Surface((self.sq_width, self.sq_height))
        self.goal_surf = pg.Surface((self.sq_width, self.sq_height))
        self.path_surf = pg.Surface((self.sq_width, self.sq_height))
        self.obstacle_surf = pg.Surface((self.sq_width, self.sq_height))
        self.neutral_surf = pg.Surface((self.sq_width, self.sq_height))
        self.visited_surf = pg.Surface((self.sq_width, self.sq_height))
        self.start_surf.fill("Green")
        self.goal_surf.fill("Red")
        self.path_surf.fill("Blue")
        self.obstacle_surf.fill("Grey")
        self.neutral_surf.fill("White")
        self.visited_surf.fill("Yellow")

        # creates grid of neutral squares
        neutral_squares = []
        for i in range(self.board.height):
            for j in range(self.board.width):
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

    def clear(self):
        """Removes shown path."""
        self.showed_path = []
        self.showed_visited_sq = []
        self.running = False
        self.cleared = True

    def run(self):
        """Begins visualization of path."""
        if self.start and self.goal:
            self.running = True
            self.cleared = False

    def pause(self):
        """Pauses visualization of path."""
        self.running = False

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
                    if self.run_button_rect.collidepoint(event.pos):
                        self.run()
                    # pause path visualization
                    elif self.pause_button_rect.collidepoint(event.pos):
                        self.pause()
                    # clears shown path
                    elif self.clear_button_rect.collidepoint(event.pos):
                        self.clear()
                    # user returns to StartPage
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.clear()
                        self.board.obstacles = []
                        self.board.set_start(None)
                        self.board.set_goal(None)
                        return 0
                    # user opens InstructionsPage
                    elif self.instructions_button_rect.collidepoint(event.pos):
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

        # adds background and menu buttons to screen
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.run_button_surf, self.run_button_rect)
        self.screen.blit(self.run_text_surf, self.run_text_rect)

        self.screen.blit(self.pause_button_surf, self.pause_button_rect)
        self.screen.blit(self.pause_text_surf, self.pause_text_rect)

        self.screen.blit(self.clear_button_surf, self.clear_button_rect)
        self.screen.blit(self.clear_text_surf, self.clear_text_rect)

        self.screen.blit(self.back_button_surf, self.back_button_rect)
        self.screen.blit(self.back_text_surf, self.back_text_rect)

        self.screen.blit(self.instructions_button_surf, self.instructions_button_rect)
        self.screen.blit(self.instructions_text_surf, self.instructions_text_rect)

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
                new_x = int(self.menu_width + self.grid_marginal_width + (cord[0] - 1) * (self.sq_width + self.grid_marginal_width))
                new_y = int(self.grid_marginal_height + (cord[1] - 1) * (self.sq_height + self.grid_marginal_height))
                new_cords.append((new_x, new_y))
            else:
                new_cords.append(None)  # undersök om detta behövs och vad det leder till om det inträffar
        return new_cords

    def screen_coordinate_to_square(self, cord):
        """Converts coordinate on screen to a square on the board."""
        new_x = int((cord[0] - self.menu_width + self.sq_width) / (self.sq_width + self.grid_marginal_width))
        new_y = int((cord[1]  + self.sq_height) / (self.sq_height + self.grid_marginal_height))
        return (new_x, new_y)