import pygame
import random

pygame.init()

# Size/ 10 equal number of rows an col in maze
SIZE = 400

pygame.display.set_caption("maze generation algorithm")
WIN = pygame.display.set_mode((SIZE, SIZE))

# colors used ti display maze generation
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (161, 3, 252)
ORANGE = (255,165,0)
AQUA = (0, 255, 255)
PINK = (255,192,203)
YELLOW = (255,255,0)


maze_colors = [ORANGE, AQUA, PINK, YELLOW, WHITE]
maze_color = random.choice(maze_colors)


class cell:

    """initialize the generation of a cell give it a row col Size and total_ rows.
    Set the base color to purple and give it no neighbors"""

    def __init__(self, row, col, SIZE, total_rows):
        self.row = row
        self.col = col
        self.total_rows = total_rows
        self.SIZE = SIZE

        self.neighbors = []
        self.color = BLACK

    # get the position of the cell in the maze
    def get_pos(self):
        return (self.row, self.col)

    # if the cell is a barrier set it to black
    def is_barrier(self):
        return self.color == BLACK

    # if the cell has already been vistited set its color to white
    def is_visited(self):
        return self.color == maze_color

    # set the color of the current cell you are checking to Red
    def make_current(self):
        self.color = RED

    # if the cell is a barrier mak it a barrier bu setting its color to black
    def make_barrier(self):
        self.color = BLACK

    # her we are checking the neighbors of the cell we are currently on
    def check_neighbors(self, grid):
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

    # draw the maze and all of the cells
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.row * self.SIZE, self.col * self.SIZE, self.SIZE, self.SIZE))

    # reset the cell color to white
    def reset(self):
        self.color = maze_color

# remove barriers between neighbor cells
def remove_wall(a, b, grid):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # populate the list neighbors with the current cells neighbors
        neighbors = current.check_neighbors(grid)

        # if the current cell ha s any neighbors
        if neighbors:
            # choose a random neighbor
            choosen_one = random.choice(neighbors)
            # take the chosen cell and reset it
            choosen_one.reset()
            # remove the wall between the current an chosen cells
            grid = remove_wall(current, choosen_one, grid)
            # reset the chosen cell
            current.reset()
            # set the current cell to the chosen cell
            current = choosen_one
            # if the chosen cell is not already in the stack add it
            if choosen_one not in stack:
              stack.append(choosen_one)
        # if neighbors is empty
        else:
            # reset the current cell
            current.reset()
            # set current equal to the last entry in teh stack
            current = stack[-1]
            # remove that last entry
            stack.remove(stack[-1])
        # make the current cell red on the maze
        current.make_current()
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

# set the size of the make and create it
def main(WIN, WIDTH):
    global maze_color
    gap = 10
    grid = make_maze(WIDTH, gap, WIN)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    maze_color = random.choice(maze_colors)
                    grid = make_maze(WIDTH, gap, WIN)

        draw(WIN, WIDTH, gap, grid)


main(WIN, SIZE)