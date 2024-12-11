import random_play as rp
import numpy as np
import itertools
from concurrent.futures import ThreadPoolExecutor
import hashlib
from multiprocessing import Pool, cpu_count


# Constants for scoring
# SCORE_SUM_POWER = 2.0
# SCORE_SUM_WEIGHT = 11.0

# SCORE_LOST_PENALTY = 20000.0
# SCORE_MONOTONICITY_POWER = 3.0 # 3.0 , for depth 4
# SCORE_MONOTONICITY_WEIGHT = 60.0 # 60.0
# SCORE_MERGES_WEIGHT = 380.0 #400
# SCORE_EMPTY_WEIGHT = 270.0 # 250
# SCORE_EDGE_TILE = 2.0 # 2

SCORE_LOST_PENALTY = 200000.0
SCORE_MONOTONICITY_POWER = 3.0 
SCORE_MONOTONICITY_WEIGHT = 56.0 
SCORE_MERGES_WEIGHT = 510.0 
SCORE_EMPTY_WEIGHT = 270.0 
SCORE_EDGE_TILE = 2.0 # 2


# Tile values (including 0 for empty tiles)
TILE_VALUES = [0] + [2**i for i in range(1, 17)]  # [0, 2, 4, 8, ...131072]


# Global transposition table
transposition_table = {}

def get_board_key(grid):
    """Generate a hashable key for the current board state."""
    return hashlib.md5(grid.tobytes()).hexdigest()

def cache_result(grid, depth, score):
    """Cache the heuristic score for a board at a given depth."""
    key = get_board_key(grid)
    transposition_table[key] = (depth, score)

def get_cached_result(grid, depth):
    """Retrieve the cached score if available."""
    key = get_board_key(grid)
    if key in transposition_table:
        cached_depth, cached_score = transposition_table[key]
        if cached_depth >= depth:
            return cached_score
    return None


def calculate_heuristic_score(row):
    """Calculate heuristic score for a row."""
    # empty = row.count(0)
    empty = 0
    merges = 0
    # sum_score = sum(tile**SCORE_SUM_POWER for tile in row if tile != 0)

    # Count merges
    prev = 0
    counter = 0
    for i in range(4):
        # if row[i] == row[i + 1] and row[i] != 0:
        #     merges += 1
        #     i += 1
        rank = row[i]
        if rank == 0:
            empty += 1
        else:
            if prev == rank:
                counter += 1
            elif counter > 0:
                merges += 1 + counter
                counter = 0
            prev = rank
    if counter > 0:
        merges += 1 + counter

    # Monotonicity
    monotonicity_left = sum(
        max(0, (row[i]**SCORE_MONOTONICITY_POWER - row[i + 1]**SCORE_MONOTONICITY_POWER))
        for i in range(len(row) - 1) if row[i] > row[i + 1]
    )
    monotonicity_right = sum(
        max(0, (row[i + 1]**SCORE_MONOTONICITY_POWER - row[i]**SCORE_MONOTONICITY_POWER))
        for i in range(len(row) - 1) if row[i] < row[i + 1]
    )

    # Large values in edges
    max_edge = max(row[0], row[3])

    heuristic_score = (
        SCORE_LOST_PENALTY
        + max_edge ** SCORE_EDGE_TILE
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
    score = score + max(grid[0][0], grid[3][0], grid[0][3], grid[3][3]) ** 5
    return score

MOVES = [rp.move_left, rp.move_right, rp.move_up, rp.move_down]

def valid_moves(grid):
    """Return valid moves for the current grid."""
    return [move for move in MOVES if not np.array_equal(grid, move(grid)[0])]

def expectimax(grid, depth, maximizing_player, cprob):
    best = 0.0
    if rp.game_over(grid):
        return 0
    if depth == 0 or cprob < 0.0001:
        return evaluate(grid)

    cached_result = get_cached_result(grid, depth)
    if cached_result is not None:
        return cached_result

    if maximizing_player:
        best_score = float('-inf')
        for move in valid_moves(grid):
            new_grid, _ = move(grid)
            score = expectimax(new_grid, depth - 1, False, cprob)
            best_score = max(best_score, score)
    else:
        empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
        if not empty_cells:
            return 0
            # return evaluate(grid)
        best_score = 0
        cprob /= len(empty_cells)
        for i, j in empty_cells:
            grid[i][j] = 2
            best_score += 0.9 * expectimax(grid, depth - 1, True, cprob * 0.9)
            grid[i][j] = 4
            best_score += 0.1 * expectimax(grid, depth - 1, True, cprob * 0.1)
            grid[i][j] = 0
        best_score /= len(empty_cells)

    cache_result(grid, depth, best_score)
    return best_score


def best_move(grid, depth):
    """Find the best move using expectimax."""
    best_score = float('-inf')
    best_move = None
    for move in valid_moves(grid):
        new_grid, _ = move(grid)            
        score = expectimax(new_grid, depth - 1, False, 1.0)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def count_unique_tiles(grid):
    unique_tiles = np.unique(grid)  # Get unique elements in the grid
    unique_non_zero_tiles = unique_tiles[unique_tiles > 0]  # Filter out zeros
    return len(unique_non_zero_tiles)

def simulate_game_expectimax(depth=3):
    grid = rp.init_grid()
    game_score = 0
    for _ in range(2):  
        rp.add_new_tile(grid)

    while not rp.game_over(grid):
        # depth = max(3, count_unique_tiles(grid) - 2)
        move = best_move(grid, depth)
        grid, score = move(grid)
        game_score += score
        rp.add_new_tile(grid)
    # print("game over")
    return np.max(grid), game_score

def test_expectimax(num_games, depth=3):
    """Run multiple simulations in parallel using multiprocessing."""
    # Use all available CPU cores
    num_processes = cpu_count()

    # Create a pool of workers
    with Pool(processes=num_processes) as pool:
        # Run the simulate_game_expectimax function in parallel
        results = pool.starmap(simulate_game_expectimax, [(depth,) for _ in range(num_games)])
    
    # Aggregate results
    max_tile_results = [result[0] for result in results]
    score_results = [result[1] for result in results]

    print(f"Simulated {num_games} games.")
    print(f"Average Game Score: {np.mean(score_results)}")
    print(f"Average Maximum Tile: {np.mean(max_tile_results)}")
    print(f"Max Tile Distribution: {np.unique(max_tile_results, return_counts=True)}")

    return max_tile_results, score_results