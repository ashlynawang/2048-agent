import numpy as np
import random
import itertools
import random_play as rp

# Simulate a game with a specific move cycle
def simulate_with_cycle(grid, cycle):
    # grid = init_grid()
    cycle_index = 0
    while not rp.game_over(grid):
        move = cycle[cycle_index]
        new_grid = move(grid)
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            rp.add_new_tile(grid)
        cycle_index = (cycle_index + 1) % len(cycle)  # Repeat the cycle
    
    return np.max(grid), np.sum(grid)


def evaluate_all_cycles():
    moves = [rp.move_left, rp.move_right, rp.move_up, rp.move_down]
    move_names = ["left", "right", "up", "down"]
    permutations = list(itertools.permutations(moves))
    permutation_names = list(itertools.permutations(move_names))
    
    max_tile_results = []
    score_results = []
    for i, cycle in enumerate(permutations):
        cycle_max_results, cycle_score_results = rp.run_simulations(simulate_with_cycle, cycle)
        max_tile_results.append((permutation_names[i], cycle_max_results))
        score_results.append((permutation_names[i], cycle_score_results))
    return max_tile_results, score_results

