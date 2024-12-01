import random_play as rp
import numpy as np

def heuristic(grid):
    """Heuristic function to evaluate the grid state."""
    empty_cells = np.sum(grid == 0)
    max_tile = np.max(grid)
    smoothness = -np.sum(np.abs(np.diff(grid, axis=0))) - np.sum(np.abs(np.diff(grid, axis=1)))
    return empty_cells + max_tile + smoothness

def get_possible_moves(grid):
    """Returns all possible moves for the current grid."""
    moves = [rp.move_left, rp.move_right, rp.move_up, rp.move_down]
    possible_moves = []
    for move in moves:
        new_grid = np.copy(grid)
        new_grid_after_move = move(new_grid)
        if not np.array_equal(grid, new_grid_after_move):
            possible_moves.append((move, new_grid_after_move))
    return possible_moves

def get_possible_spawns(grid):
    """Returns all possible tile spawns with their probabilities."""
    empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    spawns = []
    for (i, j) in empty_cells:
        for value, prob in [(2, 0.9), (4, 0.1)]:
            new_grid = np.copy(grid)
            new_grid[i][j] = value
            spawns.append((new_grid, prob))
    return spawns

def expectimax(grid, depth, is_maximizing):
    """Expectimax implementation."""
    if depth == 0 or rp.game_over(grid):
        return heuristic(grid)

    if is_maximizing:
        # Player's turn: maximize score
        max_eval = float('-inf')
        for _, child_grid in get_possible_moves(grid):
            eval = expectimax(child_grid, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        # Game's turn: average over all possible spawns
        expected_value = 0
        spawns = get_possible_spawns(grid)
        if not spawns:  # No empty cells available to spawn new tiles
            return heuristic(grid)
        for spawn_grid, prob in spawns:
            eval = expectimax(spawn_grid, depth - 1, True)
            expected_value += prob * eval
        return expected_value

def find_best_move(grid, depth=3):
    """Finds the best move using expectimax."""
    best_move = None
    best_value = float('-inf')

    for move, child_grid in get_possible_moves(grid):
        value = expectimax(child_grid, depth - 1, False)
        if value > best_value:
            best_value = value
            best_move = move

    return best_move

