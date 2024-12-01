import random_play as rp 
import numpy as np


# Evaluation function
def evaluate(grid):
    """Heuristic evaluation of the grid."""
    max_tile = np.max(grid)  # Reward higher tiles
    empty_spaces = np.sum(grid == 0)  # Reward more empty spaces
    return 0.5 * max_tile + empty_spaces * 2  # Adjust weights as needed

# Minimax function
def minimax(grid, depth, maximizing_player):
    if depth == 0 or rp.game_over(grid):
        return evaluate(grid), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move_func in [rp.move_left, rp.move_right, rp.move_up, rp.move_down]:
            new_grid = move_func(grid)
            if not np.array_equal(grid, new_grid):  # Only consider valid moves
                eval_score, _ = minimax(new_grid, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move_func
        return max_eval, best_move
    else:
        min_eval = float('inf')
        empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
        for i, j in empty_cells:
            for value in [2, 4]:  # Tile values are 2 or 4
                grid_copy = grid.copy()
                grid_copy[i][j] = value
                eval_score, _ = minimax(grid_copy, depth - 1, True)
                min_eval = min(min_eval, eval_score)
        return min_eval, None

# Simulate a game using Minimax
def simulate_game_minimax(grid, depth=3):
    while not rp.game_over(grid):
        _, best_move = minimax(grid, depth, maximizing_player=True)
        if best_move:
            new_grid = best_move(grid)
            if not np.array_equal(grid, new_grid):
                grid = new_grid
                rp.add_new_tile(grid)
        else:
            break  # No valid moves
    return np.max(grid), np.sum(grid)

# Run simulations with Minimax
def run_minimax_simulations(num_games=100, depth=3):
    max_tile_results = []
    score_results = []
    for _ in range(num_games):
        grid = rp.init_grid()
        max_tile, score = simulate_game_minimax(grid, depth)
        max_tile_results.append(max_tile)
        score_results.append(score)
    return max_tile_results, score_results

