import pygame
import random

pygame.init()

SIZE = 400
pygame.display.set_caption("path_finder")
WIN = pygame.display.set_mode((SIZE, SIZE))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (242, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (161, 3, 252)
AQUA = (0, 255, 255)
BLUE = (0,0,255)


class cell:
    def __init__(self, row, col, SIZE, total_rows):
        # variables for displaying
        self.row = row
        self.col = col
        self.total_rows = total_rows
        self.SIZE = SIZE
        self.color = BLACK

        # variables for a_star_algorithm
        self.f_score = float("inf")
        self.g_score = float("inf")
        self.camefrom = None
        self.neighbors = []

        # for generating the maze
        self.visited = False

    # get the position of the cell in the maze
    def get_pos(self):
        return (self.row, self.col)

    # if the cell is a barrier set it to black
    def is_barrier(self):
        return self.color == BLACK

    # if the cell is the start cell set its color to green
    def is_start(self):
        return self.color == GREEN

    # if the cell is the end cell set its color to red
    def is_end(self):
        return self.color == RED

    # check to see if the cell has been visited
    def is_visited(self):
        return self.visited
    # if the cell has been visited set visited to True
    def make_visited(self):
        self.visited = True
    # set the current cells color to red
    def make_current(self):
        self.color = RED
    # make the final path purple
    def make_path(self):
        self.color = PURPLE
    # make the barrier cells black
    def make_barrier(self):
        self.color = BLACK

    # make the start cell. set color to green and the f and h score to 0
    def make_start(self):
        self.color = GREEN
        self.f_score = 0
        self.g_score = 0
    # make open cells AQUA
    def make_open(self):
        self.color = AQUA
    # make closed cells blue
    def make_closed(self):
        self.color = BLUE
    # make the ending cell red
    def make_end(self):
        self.color = RED

    def update_neighbors(self, grid):  # updating the neighbors for a_star algortihm

        """if the current row of the cell is not one of the cell edges and the cell one row down
                         is not a barrier make it a neighbor"""
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        """if the current row of the cell is not one of the cell edges and the cell one row up
                                 is not a barrier make it a neighbor"""
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        """if the current col of the cell is not one of the cell edges and the cell one col to the right
                                 is not a barrier make it a neighbor"""
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        """if the current col of the cell is not one of the cell edges and the cell one col to the left
                                         is not a barrier make it a neighbor"""
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def check_neighbors(self, grid):  # returns the neighbors which are not visted(for making the maze)
        neighbors = []

        """if the current row of the cell is not one of the cell edges and the cell two rows down has
                 not been visited make it a neighbor"""
        if self.row < self.total_rows - 2 and not grid[self.row + 2][self.col].is_visited():
            neighbors.append(grid[self.row + 2][self.col])
        """if the current row of the cell is greater than one (so not one of the top available cells) and the cell 2 rows
        above it has not been visited make it a neighbor"""
        if self.row > 1 and not grid[self.row - 2][self.col].is_visited():
            neighbors.append(grid[self.row - 2][self.col])
        """if the current col of the cell is not one of the maze edges and the cell two cols to the right has
                 not been visited make it a neighbor"""
        if self.col < self.total_rows - 2 and not grid[self.row][self.col + 2].is_visited():
            neighbors.append(grid[self.row][self.col + 2])
        """if the current col of the cell is greater than one (so not one of the top available cells) and the cell 2 cols
               to the left has not been visited make it a neighbor"""
        if self.col > 1 and not grid[self.row][self.col - 2].is_visited():
            neighbors.append(grid[self.row][self.col - 2])

        return neighbors

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.row * self.SIZE, self.col * self.SIZE, self.SIZE, self.SIZE))

    def reset(self):
        if self.is_start():
            self.f_score = float("inf")
            self.g_score = float("inf")
        self.color = WHITE


def remove_wall(a, b, grid):  # removes the barrier between the current cell and chosen_one
    x = (a.row + b.row) // 2
    y = (a.col + b.col) // 2
    grid[x][y].reset()
    return grid



# make the maze using recursive backtracking
def make_maze(WIDTH, gap, WIN):
    # set the size of the grid
    rows = WIDTH // gap
    # populate the grid with cells
    grid = [[cell(i, j, gap, rows) for j in range(rows)] for i in range(rows)]

    stack = []
    # make all of the outside edges of the maze be barriers and every second cell in the maze be a barrier
    for i in range(0, rows, 2):
        for j in range(rows):
            grid[i][j].make_barrier()
            grid[j][i].make_barrier()
    # set the current cell to (1,1) in the maze
    current = grid[1][1]
    # append the current cell the to stack list
    stack.append(current)
    # while stack is not empty
    while stack:
        # if a user hits the exit button quit the program
        quit()
        # populate the list neighbors with the current cells neighbors
        neighbors = current.check_neighbors(grid)

        # if the current cell ha s any neighbors
        if neighbors:
            # choose a random neighbor
            choosen_one = random.choice(neighbors)
            # take the chosen cell and make it visited
            choosen_one.make_visited()
            # remove the wall between the current an chosen cells
            grid = remove_wall(current, choosen_one, grid)
            # make the current cell visited
            current.make_visited()
            # set the current cell to the chosen cell
            current = choosen_one
            # if the chosen cell is not already in the stack add it
            if choosen_one not in stack:
              stack.append(choosen_one)
        # if neighbors is empty
        else:
            # make the current cell visited
            current.make_visited()
            # set current equal to the last entry in teh stack
            current = stack[-1]
            # remove that last entry
            stack.remove(stack[-1])
            # make the current cell red on the maze
        current.make_current()

        # make the current cell red on the maze
        # update the make and draw the new cells
        draw(WIN, WIDTH, gap, grid)
        # reset the current cell
        current.reset()
    return grid

# draw the updated cells
def draw(WIN, WIDTH, gap, grid):
    for rows in grid:
        for cells in rows:
            cells.draw(WIN)

    for i in range(0, WIDTH, gap):
        pygame.draw.line(WIN, BLACK, (0, i), (WIDTH, i))
        pygame.draw.line(WIN, BLACK, (i, 0), (i, WIDTH))

    pygame.display.update()


def h(p1, p2):  # heuristic function
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def lowest_node(open_set):  # returns the node with lowest f_score
    lowest = open_set[0]
    mini = lowest.f_score

    for node in open_set:
        if node.f_score < mini:
            mini = node.f_score
            lowest = node

    return lowest

# the A_Star algorith
def A_star(draw, grid, start, end):
    # set the first cell in the open set list
    open_set = [start]
    # if open set is not empty
    while open_set:
        # if user quits quit the program
        quit()

        #set current to the cell with the lowest f_score
        current = lowest_node(open_set)

        # if the current cell is the end cell
        if current == end:
            # set node equal to the cell that came before the current cell
            node = current.camefrom
            # while node is not the start cell
            while node != start and node:
                # if user quits quit
                quit()
                # call make path set the nodes color to purple
                node.make_path()
                # set node equal to the node the came before the previous node
                node = node.camefrom
                draw()
            return
        # remove the current cell from the open set and make it closed
        open_set.remove(current)
        current.make_closed()

        # looping through all of the current cells neighbors
        for neighbor in current.neighbors:
            # create a temp comparison g_score
            temp_g_score = current.g_score + 1
            # if the temp_g_score is lower than the neighbors g_score
            if temp_g_score < neighbor.g_score:
                # set the neighbors came from to the current cell
                neighbor.camefrom = current
                # set it's g_score to the temp_g_score
                neighbor.g_score = temp_g_score
                # set it's f_score to the temp_g_score plus the neighbors heuristic score
                neighbor.f_score = temp_g_score + h(end.get_pos(), neighbor.get_pos())
                # if the neighbor is not in the open_set append it and make it open
                if not neighbor in open_set:
                    open_set.append(neighbor)
                    neighbor.make_open()
        # sets the start and end cells
        start.make_start()
        end.make_end()
        draw()

    print("no solution")


def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


def main(WIN, WIDTH):
    gap = 10
    grid = make_maze(WIDTH, gap, WIN)
    start = None
    end = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # If the user presses the r key it creates a new maze
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = make_maze(WIDTH, gap, WIN)
                    start = None
                    end = None
                # If the user presses the space bar it runs the A star algorithm if there is a start and end node
                if event.key == pygame.K_SPACE:
                    if start and end:
                        for rows in grid:
                            for node in rows:
                                node.update_neighbors(grid)

                        A_star(lambda: draw(WIN, WIDTH, gap, grid), grid, start, end)
        # if user clicks creates the start or end cell
        if pygame.mouse.get_pressed()[0]:
            i, j = pygame.mouse.get_pos()
            i //= gap
            j //= gap
            spot = grid[i][j]
            if not start and spot != end and not spot.is_barrier():
                spot.make_start()
                start = spot
            elif not end and spot != start and not spot.is_barrier():
                spot.make_end()
                end = spot
        # if user middle clicks (command + click on mac) remove the start and or end cells and reset them
        if pygame.mouse.get_pressed()[2]:
            i, j = pygame.mouse.get_pos()
            i //= gap
            j //= gap
            spot = grid[i][j]
            if spot == start:
                start = None
            if spot == end:
                end = None
            if not spot.is_barrier():
                spot.reset()

        draw(WIN, WIDTH, gap, grid)


main(WIN, SIZE)