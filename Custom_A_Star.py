import pygame
import random

pygame.init()

SIDE = 200
pygame.display.set_caption("A* algorithm")
WIN = pygame.display.set_mode((SIDE, SIDE))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PURPLE = (161, 3, 252)
PINK = (0, 255, 255)


class cell:
    def __init__(self, row, col, side, total_rows):
        self.row = row
        self.col = col
        self.total_rows = total_rows
        self.side = side

        self.g_score = float("inf")
        self.f_score = float("inf")
        self.camefrom = None
        self.neighbors = []
        self.color = WHITE


    #return cells position
    def get_pos(self):
        return (self.row, self.col)

    # makes a the cell a barrier cell and changes color to black
    def is_barrier(self):
        return self.color == BLACK

    # sets color of start cell
    def is_start(self):
        return self.color == BLUE

    # sets color of end cell
    def is_end(self):
        return self.color == GREEN

    # sets color of path cells
    def make_path(self):
        self.color = PURPLE

    # makes a barrier
    def make_barrier(self):
            self.color = BLACK

    # makes a start cell and initializes its f and g scores
    def make_start(self):
            self.color = BLUE
            self.f_score = 0
            self.g_score = 0



    # make open cell
    def make_open(self):
            self.color = PINK

    # make a closed cell
    def make_closed(self):
            self.color = RED

    # make an ending cell
    def make_end(self):
            self.color = GREEN

    # update the cells neighbors
    def update_neighbors(self, grid):
        # handles verical and horizontal neighbors
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

        # handles diagonal neighbors
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col - 1])

        if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col + 1])

        if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][
            self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col + 1])

        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col - 1])

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.row * self.side, self.col * self.side, self.side, self.side))

    def reset(self):
        if self.is_start():
            self.f_score = float("inf")
            self.g_score = float("inf")
        self.color = WHITE


def make_grid(WIDTH, gap):
        rows = WIDTH // gap
        return [[cell(i, j, gap, rows) for j in range(rows)] for i in range(rows)]

def draw(WIN, WIDTH, gap, grid):
    for rows in grid:
            for cells in rows:
                cells.draw(WIN)

    for i in range(0, WIDTH, gap):
        pygame.draw.line(WIN, BLACK, (0, i), (WIDTH, i))
        pygame.draw.line(WIN, BLACK, (i, 0), (i, WIDTH))

    pygame.display.update()

# hueristic function cost to reach the end cell from current cell
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def lowest_node(open_set):  # returns the node with lowest f_score
    # grabs the first cell in the open_set
    lowest = open_set[0]
    # the minimum f_score mini is the f_score_of lowest
    mini = lowest.f_score

    # loop through each cell in the open_set
    for node in open_set:
        # if a cell in open set has a f_score lower than mini set mini to that new f_score and lowest to that cell
        if node.f_score < mini:
            mini = node.f_score
            lowest = node
    return lowest


def A_star(draw, grid, start, end):
    open_set = [start]

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = lowest_node(open_set)

        if current == end:
            node = current.camefrom
            while node != start and node:
                node.make_path()
                node = node.camefrom
                draw()
            return

        open_set.remove(current)
        current.make_closed()

        for neighbor in current.neighbors:
            temp_g_score = current.g_score + 1

            if temp_g_score < neighbor.g_score:
                neighbor.camefrom = current
                neighbor.g_score = temp_g_score
                neighbor.f_score = temp_g_score + h(end.get_pos(), neighbor.get_pos())
                if not neighbor in open_set:
                    open_set.append(neighbor)
                    neighbor.make_open()

        start.make_start()
        end.make_end()
        draw()

    print("no solution")

    print("no solution")

def random_map(grid, barriers):
    choices = [[i, j] for i in range(20) for j in range(20)]
    for i in range(barriers):
        pos = random.choice(choices)
        choices.remove(pos)
        grid[pos[0]][pos[1]].make_barrier()

    return grid


def main(WIN, WIDTH):
    gap = 10
    grid = make_grid(WIDTH, gap)
    grid = random_map(grid, 0)
    start = None
    end = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    grid = make_grid(WIDTH, gap)
                    grid = random_map(grid, 0)
                    start = None
                    end = None
                if event.key == pygame.K_SPACE:
                    if start and end:
                        for rows in grid:
                            for node in rows:
                                node.update_neighbors(grid)

                        A_star(lambda: draw(WIN, WIDTH, gap, grid), grid, start, end)

        if pygame.mouse.get_pressed()[0]:
            i, j = pygame.mouse.get_pos()
            i //= gap
            j //= gap
            spot = grid[i][j]
            if not start and spot != end:
                spot.make_start()
                start = spot
            elif not end and spot != start:
                spot.make_end()
                end = spot
            elif spot != start and spot != end:
                spot.make_barrier()
        if pygame.mouse.get_pressed()[2]:
            i, j = pygame.mouse.get_pos()
            i //= gap
            j //= gap
            spot = grid[i][j]
            if spot == start:
                start = None
            if spot == end:
                end = None
            spot.reset()



        draw(WIN, WIDTH, gap, grid)


main(WIN, SIDE)
