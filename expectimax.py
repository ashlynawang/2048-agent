import random_play as rp
import numpy as np

# def evaluate(grid):
#     """Heuristic to score the grid: prioritize empty tiles and high tile values."""
#     max_tile = np.max(grid)
#     empty_cells = np.sum(grid == 0)
#     monotonicity_score = monotonicity(grid)
#     smoothness_score = smoothness(grid)
#     return max_tile + 20 * empty_cells + 0.2 * monotonicity_score - 0.4 * smoothness_score

# def monotonicity(grid):
#     """Measure monotonicity of the grid (smooth progression of numbers) for rows and columns."""
#     monotonicity = 0   
#     for vector in np.vstack([grid, grid.T]): 
#         for i in range(len(vector) - 1):
#             if vector[i] <= vector[i + 1]:  
#                 monotonicity += 1
#             elif vector[i] >= vector[i + 1]:
#                 monotonicity += 1 
#     return monotonicity

# def smoothness(grid):
#     """Measure smoothness (low adjacent differences in the grid)."""
#     smoothness = 0
#     for row in grid:
#         smoothness += sum(abs(row[i] - row[i + 1]) for i in range(len(row) - 1) if row[i] and row[i + 1])
#     for col in grid.T:
#         smoothness += sum(abs(col[i] - col[i + 1]) for i in range(len(col) - 1) if col[i] and col[i + 1])
#     return smoothness

import itertools
import numpy as np

# Constants for scoring
SCORE_LOST_PENALTY = 200000.0
SCORE_MONOTONICITY_POWER = 4.0
SCORE_MONOTONICITY_WEIGHT = 55.0
SCORE_SUM_POWER = 2.0
SCORE_SUM_WEIGHT = 11.0
SCORE_MERGES_WEIGHT = 500.0
SCORE_EMPTY_WEIGHT = 300.0

# Tile values (including 0 for empty tiles)
TILE_VALUES = [0] + [2**i for i in range(1, 13)]  # [0, 2, 4, 8, ..., 4096]

def calculate_heuristic_score(row):
    """Calculate heuristic score for a row."""
    empty = row.count(0)
    merges = 0
    sum_score = sum(tile**SCORE_SUM_POWER for tile in row if tile != 0)

    # Count merges
    i = 0
    while i < len(row) - 1:
        if row[i] == row[i + 1] and row[i] != 0:
            merges += 1
            i += 1
        i += 1

    # Monotonicity
    monotonicity_left = sum(
        max(0, (row[i]**SCORE_MONOTONICITY_POWER - row[i + 1]**SCORE_MONOTONICITY_POWER))
        for i in range(len(row) - 1) if row[i] > row[i + 1]
    )
    monotonicity_right = sum(
        max(0, (row[i + 1]**SCORE_MONOTONICITY_POWER - row[i]**SCORE_MONOTONICITY_POWER))
        for i in range(len(row) - 1) if row[i] < row[i + 1]
    )

    heuristic_score = (
        SCORE_LOST_PENALTY
        + SCORE_EMPTY_WEIGHT * empty
        + SCORE_MERGES_WEIGHT * merges
        - SCORE_MONOTONICITY_WEIGHT * min(monotonicity_left, monotonicity_right)
    )
    return heuristic_score

def precompute_scores():
    """Precompute heuristic scores for all 4-tile combinations."""
    heuristic_table = {}

    # Generate all possible 4-tile combinations
    for row in itertools.product(TILE_VALUES, repeat=4):
        heuristic_table[row] = calculate_heuristic_score(row)

    return heuristic_table

# Precompute the scores
heuristic_table = precompute_scores()

def evaluate(grid):
    score = 0
    for row in grid:
        score += heuristic_table.get(tuple(row), 0)
    for col in grid.T:
        score += heuristic_table.get(tuple(col), 0)
    return score

MOVES = [rp.move_left, rp.move_right, rp.move_up, rp.move_down]

def valid_moves(grid):
    """Return valid moves for the current grid."""
    return [move for move in MOVES if not np.array_equal(grid, move(grid))]

def expectimax(grid, depth, maximizing_player):
    if depth == 0 or rp.game_over(grid):
        return evaluate(grid)

    if maximizing_player:
        return max(expectimax(move(grid), depth - 1, False) for move in valid_moves(grid))
    else:
        empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
        if not empty_cells:
            return evaluate(grid)
        value = 0
        for i, j in empty_cells:
            grid[i][j] = 2
            value += 0.9 * expectimax(grid, depth - 1, True)
            grid[i][j] = 4
            value += 0.1 * expectimax(grid, depth - 1, True)
            grid[i][j] = 0
        return value / len(empty_cells)

def best_move(grid, depth):
    """Find the best move using expectimax."""
    best_score = float('-inf')
    best_move = None
    for move in valid_moves(grid):
        new_grid = move(grid)
        score = expectimax(new_grid, depth - 1, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def simulate_game_expectimax(depth=3):
    grid = rp.init_grid()
    for _ in range(2):  
        rp.add_new_tile(grid)

    while not rp.game_over(grid):
        move = best_move(grid, depth)
        grid = move(grid)
        rp.add_new_tile(grid)
    return np.max(grid), np.sum(grid)