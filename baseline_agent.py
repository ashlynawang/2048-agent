import numpy as np
from random_play import *

class BaselineAgent:
    def __init__(self, iterations=2000):
        self.iterations = iterations

    def choose_action(self, state):
        moves = [move_down, move_right, move_left, move_up]
        for move in moves:
            new_grid, _ = move(state)
            if not np.array_equal(state, new_grid):  # Check if the move changes the grid
                return move
    
def test_baseline_agent(num_games=100):
    grid = init_grid()
    agent = BaselineAgent()
    scores = []
    max_tiles = []
    for i in range(num_games):
        score = 0
        grid = init_grid()
        while not game_over(grid):
            action = agent.choose_action(grid)
            new_grid, added_score = action(grid)
            score += added_score
            if not np.array_equal(grid, new_grid):
                grid = new_grid
                add_new_tile(grid)
            
        # print("Max Tile Achieved by Baseline:", np.max(grid))
        # print("Score Achieved by Baseline:", score)
        scores.append(score)
        max_tiles.append(np.max(grid))
    
    print("Average Score Achieved by Baseline:", np.mean(scores))
    unique_tiles, counts = np.unique(max_tiles, return_counts=True)
    tile_distribution = {tile: count for tile, count in zip(unique_tiles, counts)}
    print(f"Max Tile Distribution: {tile_distribution}")
    print(f"Average Max Tile: {np.mean(max_tiles)}")

if __name__ == "__main__":
    test_baseline_agent()