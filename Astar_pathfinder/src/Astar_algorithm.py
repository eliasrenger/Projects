# External imports
from queue import PriorityQueue
import random as rn

class Board():
    """The 2D space we are navigating based on squares."""
    def __init__(self):
        self.width = None
        self.height = None
        self.obstacles = []
        self.start = None
        self.goal = None
        self.geometry_changed = False
        self.squares_changed = False

    def set_geometry(self, width, height):
        self.width = width
        self.height = height
        self.start = None
        self.goal = None
        self.geometry_changed = True

    def geometry_change(self, changed):
        self.geometry_changed = changed #True or False

    def set_start(self, cord):
        if cord:
            x = cord[0]
            y = cord[1]
            is_goal = ((x,y) == self.goal)
            if self.walkable_square(x, y) and not is_goal:
                self.start = (x, y)
                self.squares_changed = True
        else:
            self.start = None
            self.squares_changed = True

    def set_goal(self, cord):
        if cord:
            x = cord[0]
            y = cord[1]
            is_start = ((x,y) == self.start)
            if self.walkable_square(x, y) and not is_start:
                self.goal = (x, y)
                self.squares_changed = True
        else:
            self.goal = None
            self.squares_changed = True

    def add_obstacle(self, cord):
        if self.walkable_square(cord[0], cord[1]):  #Makes sure duplicates or coordinates that are not on the defined board are not added
            self.obstacles.append(cord)
        self.squares_changed = True

    def remove_obstacle(self, cord):
        self.obstacles.remove(cord)
        self.squares_changed = True

    def randomize_obstacles(self):
        self.obstacles = []
        probability = rn.uniform(3, 10)
        for i in range(self.width):
            for j in range(self.height):
                a, b = i+1, j+1
                is_obstacle = rn.choices([True, False], [probability, 10-probability])[0]
                is_start_goal = ((a, b) == self.start or (a, b) == self.goal)
                if is_obstacle and not is_start_goal:
                    self.add_obstacle((a, b))
        self.squares_changed = True

    def randomize_start_goal(self):
        self.start, self.goal = None, None
        while not (self.start and self.goal):
            self.set_start((rn.randint(1, self.width + 1), rn.randint(1, self.height+ 1)))
            self.set_goal((rn.randint(1, self.width + 1), rn.randint(1, self.height + 1)))
        self.squares_changed = True

    def walkable_square(self, x, y):
        """Checks if input coordinate is a free space on the board."""
        onboard = (0 < x <= self.width) and (0 < y <= self.height)
        obstacle = ((x, y) in self.obstacles)
        if onboard and not obstacle and (type(x) == int and type(y) == int):
            return True
        else:
            return False

    def create_children(self, current):
        children = []
        position = current[2]
        current_path = current[3][:]
        current_scost = current[1]
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = position[0] + i
                y = position[1] + j
                if len(current_path) > 1:
                    is_parent = (x == current_path[-2][0] and y == current_path[-2][1]) #är det samma som att den inte ska stanna på samma ruta
                else:
                    is_parent = False
                if (i == 0 and j == 0) or is_parent or not self.walkable_square(x, y):
                    continue
                added_scost = getdist((x, y), position)
                scost = added_scost + current_scost
                gcost = getdist((x, y), self.goal)
                hcost = round(scost + gcost, 4)
                children.append((hcost, scost, (x, y), current_path + [(x, y)]))
        return children

    def pathfinder(self):
        if self.start and self.goal:
            current = [None, 0, self.start, [self.start]]
            path = []
            visited_queue = [self.start]
            q = PriorityQueue()
            while not path:
                children = self.create_children(current)
                for child in children:
                    q.put(child)
                while current[2] in visited_queue:
                    if q.empty():
                        return None, visited_queue
                    current = q.get()
                visited_queue.append(current[2])
                if current[2] == self.goal:
                    path = current[3]
            return path, visited_queue
        else:
            return None, []


def getdist(cord1, cord2):
    """Distance between start-square and input-square"""
    dist_x = abs(cord1[0] - cord2[0])
    dist_y = abs(cord1[1] - cord2[1])
    closest_axis = min(dist_x, dist_y)
    distance = 1.4 * closest_axis + dist_x + dist_y - 2 * closest_axis
    return distance

if __name__ == "__main__":
    height = 10
    width = 10
    board = Board()
    board.set_geometry(width, height)
    board.set_start(4, 1)
    board.set_goal(5, 7)
    board.add_obstacles([(3, 4), (3, 5), (4, 3), (4, 4), (5, 4), (6, 4), (2, 4), (6, 5), (6, 6), (6, 7), (7, 7)])
    path = board.pathfinder()
    print(path)