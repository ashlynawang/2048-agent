import math
import random
import numpy as np
import multiprocessing
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

from random_play import *


MOVES = [move_down, move_right, move_left, move_up]

def simulate_memory_games(grid):
    total_score = 0
    move_history = []
    moves = [move_left, move_right, move_up, move_down]

    while not game_over(grid):
        move = random.choice(moves)
        new_grid, game_score = move(grid)
        total_score += game_score
        move_history.append(move)
        
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            add_new_tile(grid)
    
    return move_history[0], total_score

def simulate_wrapper(grid):
    return simulate_memory_games(grid)

def mcts(grid, n_simulations):
    results = defaultdict(list)

    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        # Pass the grid to each process for simulation
        simulations = list(executor.map(simulate_wrapper, [grid] * n_simulations))

    for first_move, game_score in simulations:
        results[first_move].append(game_score)

    # Get average scores to determine the best move
    score_avgs = {key: sum(values) / len(values) for key, values in results.items()}
    best_move = max(score_avgs, key=score_avgs.get)
    return best_move


# def mcts(grid, n_simulations):
#     results = defaultdict(list)
#     for _ in range(n_simulations):
#         first_move, game_score = simulate_memory_games(grid)
#         results[first_move].append(game_score)
    
#     score_avgs = {key: sum(values) / len(values) for key, values in results.items()}
#     best_move = max(score_avgs, key=score_avgs.get)
#     return best_move

class MCTSAgent:
    def __init__(self, n_simulations=500):
        self.n_simulations = n_simulations
        self.moves = [move_down, move_right, move_left, move_up]

    def choose_action(self, grid):
        best_move = mcts(grid, self.n_simulations)
        return best_move

def simulate_mcts(num_games):
    agent = MCTSAgent()
    score = 0
    grid = init_grid()

    while not game_over(grid):
        action = agent.choose_action(grid)
        new_grid, added_score = action(grid)
        score += added_score
        score += max(grid[0][3], grid[3][0], grid[0][0], grid[3][3]) * 0.2
        if not np.array_equal(grid, new_grid):
            grid = new_grid
            add_new_tile(grid)
    
    max_tile = np.max(grid)
    # print(f"Game Over!")  
    # print("Max Tile Achieved by MCTS:", max_tile)
    # print("Score Achieved by MCTS:", score)
    return max_tile, score
    

def test_mcts(num_games):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(simulate_mcts, range(num_games)))

    max_tiles, scores = zip(*results)  # Separate max tiles and scores
    print("Parallel Simulation Complete!")
    print(f"Max Tile Distribution: {np.unique(max_tiles, return_counts=True)}")
    print(f"Average Max Tile: {np.mean(max_tiles)}")
    print(f"Average Score: {np.mean(scores)}")
    return max_tiles, scores

# state_cache = {}  # {grid_key: (reward, visits, depth)}

# def grid_to_key(grid):
#     return tuple(map(tuple, grid))

# def get_cached_value(state, depth):
#     k = grid_to_key(state)
#     if k in state_cache:
#         avg_reward, visits, cached_depth = state_cache[k]
#         # Use cached value only if cached_depth >= depth, meaning we've evaluated
#         # this state at least as deep as we are now.
#         if cached_depth >= depth:
#             return avg_reward, visits
#     return None

# def update_cache(state, avg_reward, visits, depth):
#     k = grid_to_key(state)
#     # Only update if this evaluation is at a greater or equal depth than what’s stored
#     if k not in state_cache or state_cache[k][2] < depth:
#         state_cache[k] = (avg_reward, visits, depth)

# def simulate_parallel(states):
#     with multiprocessing.Pool() as pool:
#         results = pool.map(simulate_game, states)
#     return results

# def parallel_simulation_phase(node, num_simulations):
#     states = [node.state for _ in range(num_simulations)]
#     rewards = simulate_parallel(states)
#     return rewards


# # Monte Carlo Tree Search
# class Node:
#     def __init__(self, state, parent=None, action=None):
#         self.reward = 0.0
#         self.visits = 0
#         self.state = state
#         self.children = {}
#         self.parent = parent
#         self.action = action
#         self.untried_actions = [move_left, move_right, move_up, move_down]
#         if parent is None:
#             self.depth = 0
#         else:
#             self.depth = parent.depth + 1
#     def is_fully_expanded(self):
#         """ Check if all possible actions have been expanded (left right up down) """
#         return len(self.children) == 4

#     def best_child(self):
#         """ Returns best child found using UCB1. """

#         def ucb1(node):
#             return (node.reward / node.visits) + np.sqrt(2 * np.log(self.visits) / node.visits)
#         return max(self.children.values(),  key=ucb1)
    
#     def expand(self):
#         actions = [move_left, move_right, move_up, move_down]
#         random.shuffle(actions)
#         for action in actions:
#             new_state, _ = action(self.state)
#             if not np.array_equal(new_state, self.state): # only expand valid moves, return the first new state
#                 child = Node(new_state, parent=self, action=action)
#                 self.children[action] = child
#                 return child
#         return self
    
#     def playout(self, max_depth=20):
#         curr_state = self.state
#         depth = 0
#         while not game_over(curr_state) and depth < max_depth:
#             moves = [move_down, move_right, move_left, move_up]
#             # random.shuffle(moves)
#             # move = random.choice(moves)
#             for move in moves:
#                 new_state, _ = move(curr_state)
#                 if not np.array_equal(new_state, curr_state): 
#                     curr_state = new_state
#                     add_new_tile(curr_state)
#                     break # break after first valid move

#             depth += 1
#         return np.max(curr_state), np.sum(curr_state)


# def select(node):
#     while not game_over(node.state) and node.is_fully_expanded():
#         node = node.best_child()
#     return node

# def backpropagate(node, reward):
#     while node is not None:
#         node.visits += 1
#         node.reward += reward 
#         node = node.parent


# def mcts(root, iterations=1000, max_time=1):
#     # for _ in range(iterations):
#     start_time = time.time()
#     iterations = 0
#     while time.time() - start_time < max_time:
#         iteration_start_time = time.time()
#         # Traverse by UCB
#         leaf = select(root)
#         if not game_over(leaf.state):
#             leaf = leaf.expand()
        
#         playout_start_time = time.time()
#         max_tile, score = leaf.playout()
#         # print(f"Playout took {time.time() - playout_start_time} seconds")
#         backpropagate(leaf, score)

#         # print(f"Iteration {iterations} took {time.time() - iteration_start_time} seconds")
#         iterations += 1

#     print(f"Number of iterations for one move = {iterations}")
    

    
#     best_reward = -math.inf
#     for action, node in root.children.items():
#         if node.visits == 0:
#             continue
#         new_state, _ = action(root.state)
#         if not np.array_equal(new_state, root.state):
#             new_reward = node.reward / node.visits
#             if new_reward > best_reward:
#                 best_reward = new_reward
#                 best_action = action

#     print("MCTS finished")
#     return best_action
        
# class MCTSAgent:
#     def __init__(self, iterations=2000):
#         self.iterations = iterations

#     def choose_action(self, state):
#         root = Node(state)
#         best_action = mcts(root, self.iterations)
#         return best_action

# def test_MCTS(num_games):
#     grid = init_grid()
#     agent = MCTSAgent()
#     scores = []
#     for i in range(num_games):
#         score = 0
#         grid = init_grid()
#         while not game_over(grid):
#             action = agent.choose_action(grid)
#             new_grid, added_score = action(grid)
#             score += added_score
#             if not np.array_equal(grid, new_grid):
#                 grid = new_grid
#                 add_new_tile(grid)

#         print(f"Game {i} Over!")  
#         print("Max Tile Achieved by MCTS:", np.max(grid))
#         print("Score Achieved by MCTS:", score)
#         scores.append(score)
    
#     print("Average Score Achieved by MCTS:", np.mean(scores))
    
# if __name__ == "__main__":
#     num_games = 10
#     test_MCTS(num_games)


