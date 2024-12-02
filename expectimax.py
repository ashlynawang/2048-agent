import random_play as rp
import numpy as np

def evaluate(grid):
    """Heuristic to score the grid: prioritize empty tiles and high tile values."""
    max_tile = np.max(grid)
    empty_cells = np.sum(grid == 0)
    monotonicity_score = monotonicity(grid)
    smoothness_score = smoothness(grid)
    return max_tile + 2 * empty_cells + 0.4 * monotonicity_score - 0.2 * smoothness_score

def monotonicity(grid):
    """Measure monotonicity of the grid (smooth progression of numbers) for rows and columns."""
    monotonicity = 0   
    for vector in np.vstack([grid, grid.T]): 
        for i in range(len(vector) - 1):
            if vector[i] <= vector[i + 1]:  
                monotonicity += 1
            elif vector[i] >= vector[i + 1]:
                monotonicity += 1 
    return monotonicity

def smoothness(grid):
    """Measure smoothness (low adjacent differences in the grid)."""
    smoothness = 0
    for row in grid:
        smoothness += sum(abs(row[i] - row[i + 1]) for i in range(len(row) - 1) if row[i] and row[i + 1])
    for col in grid.T:
        smoothness += sum(abs(col[i] - col[i + 1]) for i in range(len(col) - 1) if col[i] and col[i + 1])
    return smoothness

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