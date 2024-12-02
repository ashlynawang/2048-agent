import random
import numpy as np
import itertools


def add_new_tile(grid):
    """ Adds a new tile randomly to the available sqaures. '2' with prob 0.9, '4' with prob 0.1 """
    empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = 2 if random.random() < 0.9 else 4


def merge_tiles(row):
    """ Slides all non-zero tiles to the left and merges equal ones. """
    row = [tile for tile in row if tile != 0]
    for i in range(len(row)-1):
        if row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0

    # Realign tiles to the left
    row = [tile for tile in row if tile != 0]
    row += [0] * (4 - len(row))
    return np.array(row)


def move_left(grid):
    return np.array([merge_tiles(row) for row in grid])


def move_right(grid):
    return np.array([merge_tiles(row[::-1])[::-1] for row in grid])


def move_up(grid):
    transposed = np.transpose(grid)
    moved = np.array([merge_tiles(row) for row in transposed])
    return np.transpose(moved)


def move_down(grid):
    transposed = np.transpose(grid)
    moved = np.array([merge_tiles(row[::-1])[::-1] for row in transposed])
    return np.transpose(moved)


def game_over(grid):
    if any(0 in row for row in grid):
        return False
    for move in [move_left, move_right, move_up, move_down]:
        if not np.array_equal(grid, move(grid)):
            return False         
    return True


def init_grid():
    grid = np.zeros((4, 4))
    add_new_tile(grid)
    add_new_tile(grid)
    return grid


def simulate_game(grid):
    moves = [move_left, move_right, move_up, move_down]

    while not game_over(grid):
        move = random.choice(moves)
        new_grid = move(grid)
        
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            add_new_tile(grid)
    
    return np.max(grid), np.sum(grid)


def run_simulations(simulation, cycle=None, num_games=1000):
    max_tile_results = []
    score_results = []
    for _ in range(num_games):
        grid = init_grid()
        max_tile, score = simulation(grid) if not cycle else simulation(grid, cycle)
        max_tile_results.append(max_tile)
        score_results.append(score)
    return max_tile_results, score_results