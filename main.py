# Eric Li, Ashlyn Wang
# CPSC 474 Final Project: 2048 Agent using Expectimax and MCTS
# 
# For this project, we implemented two different AI agents to play the game 2048. 2048 is played on a 4x4 grid where the player can slide tiles in four directions: up, down, left, and right. When two tiles with the same number touch, they merge into one tile with a value equal to the sum of the two tiles. The goal of the game is to create a tile with the value of 2048. The game ends when there are no valid moves left. Whenver the player makes a new tile, they earn its value in points (i.e. when combining two 8's the player earns 16 points). The total score is the player's score when the game ends.
# We try to determine how well each agent performs when compared to a ruled-based agent that obeyes the following strategy: moves down and right repeatedly. If down and right aren't valid moves, move left. If no other moves are valid, move up. 
# Results: 2000 iterations per move MCTS agent average points over 100 games: 2594.0
# Expectimax depth=X average points over 100 games:
# Rule-based baseline agent average points over 100 games: 2685.76

import numpy as np
import random_play as rp
import cyclic_play as cp
import minimax as mm
import expectimax
import time
import mcts
import baseline_agent


if __name__ == "__main__":
    # Expectimax
    num_games = 10  
    depth = 5  
    expectimax.test_expectimax(num_games, depth)

    # MCTS
    num_games = 5
    mcts.test_MCTS(num_games)

    # Rule-based baseline agent
    baseline_agent.test_baseline_agent(num_games)
   








