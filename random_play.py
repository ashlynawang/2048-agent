import random
import numpy as np
import itertools

def add_new_tile(grid):
    """Adds a new tile to a random empty cell."""
    empty_cells = np.argwhere(grid == 0)
    if empty_cells.size > 0:
        i, j = empty_cells[np.random.choice(len(empty_cells))]
        grid[i, j] = 2 if random.random() < 0.9 else 4

def merge_tiles(row):
    """Optimized sliding and merging of tiles in a single row."""
    non_zero = row[row != 0]  # Filter non-zero tiles
    merged = np.zeros_like(row)  # Preallocate merged row
    idx = 0  # Index to fill merged row

    i = 0
    while i < len(non_zero):
        if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:  # Merge condition
            merged[idx] = non_zero[i] * 2
            i += 2  # Skip the next tile
        else:
            merged[idx] = non_zero[i]
            i += 1
        idx += 1

    return merged

def move_left(grid):
    """Move tiles left with optimized row processing."""
    return np.array([merge_tiles(row) for row in grid])

def move_right(grid):
    """Move tiles right with optimized row processing."""
    return np.array([merge_tiles(row[::-1])[::-1] for row in grid])

def move_up(grid):
    """Move tiles up."""
    return move_left(grid.T).T

def move_down(grid):
    """Move tiles down."""
    return move_right(grid.T).T



def game_over(grid):
    """Check if there are no valid moves."""
    if 0 in grid:
        return False
    for i in range(4):
        for j in range(3):
            # Check horizontal and vertical neighbors
            if grid[i, j] == grid[i, j + 1] or grid[j, i] == grid[j + 1, i]:
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