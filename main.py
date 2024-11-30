import random
import numpy as np 


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
    return row + [0] * (4 - len(row))


def move_left(grid):
    return [merge_tiles(row) for row in grid]


def move_right(grid):
    return [merge_tiles(row[::-1])[::-1] for row in grid]


def move_up(grid):
    transposed = np.transpose(grid)
    moved = [merge_tiles(row) for row in transposed]
    return np.transpose(moved)


def move_down(grid):
    transposed = np.transpose(grid)
    moved = [merge_tiles(row[::-1])[::-1] for row in transposed]
    return np.transpose(moved)


def game_over(grid):
    if any(0 in row for row in grid):
        return False
    for move in [move_left, move_right, move_up, move_down]:
        if not np.array_equal(grid, move(grid)):
            return False         
    return True


def simulate_game():
    grid = np.zeros((4, 4))
    add_new_tile(grid)
    add_new_tile(grid)
    moves = [move_left, move_right, move_up, move_down]

    while not game_over(grid):
        move = random.choice(moves)
        new_grid = move(grid)
        
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            add_new_tile(grid)
    
    return grid, max(max(row) for row in grid)


def run_simulations(num_games=100):
    results = []
    for _ in range(num_games):
        _, max_tile = simulate_game()
        results.append(max_tile)
    return results


if __name__ == "__main__":
    results = run_simulations()
    print("Average Max Tile:", sum(results) / len(results))
    print("Tile Distribution:", {tile: results.count(tile) for tile in set(results)})



