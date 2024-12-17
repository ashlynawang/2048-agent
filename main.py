# Eric Li, Ashlyn Wang
# CPSC 474 Final Project: 2048 Agent using Expectimax and MCTS

import numpy as np
import random_play as rp
# import cyclic_play as cp
# import minimax as mm
import expectimax
import time
import mcts
import baseline_agent
import argparse



if __name__ == "__main__":
    # Project overview
    print("For this project, we implemented two different AI agents to play the game 2048. 2048 is played on a 4x4 grid where the player can slide the entire grid in four directions: up, down, left, and right. When two tiles with the same number touch, they merge into one tile with a value equal to the sum of the two tiles. The goal of the game is to create a tile with the value of 2048. The game ends when there are no valid moves left. Whenver the player makes a new tile, they earn its value in points (i.e. when combining two 8's the player earns 16 points). The total score is the player's score when the game ends.")
    print("In our code, we implement our own model of 2048. We represent the grid as a 2D array and implement the user actions as well as the logic for merging tiles and adding new tiles. For the agents, we implement an Expectimax agent, which can run with various depths, as well as a MCTS agent. We try to determine how well each agent performs when compared to a ruled-based agent that obeys the following strategy: moves down and right repeatedly. If down and right aren't valid moves, move left. If no other moves are valid, move up. ")
    print("Results: We measure the average score each agent achieves as well as the percentage distribution of the maximum tile that the agent achieves in the simulated games.\n")
    print("MCTS agent average score and max tile distribution over 1000 games: 42482.08, {512: 0.019, 1024: 0.101, 2048: 0.699, 4096: 0.181}")
    print("Expectimax depth=5 average score and max tile distribution over 1000 games: 30674.16, {256: 0.041, 512: 0.019, 1024: 0.120, 2048: 0.365, 4096: 0.275}")
    print("Rule-based baseline agent average score and max tile distribution over 1000 games: 2685.76, {64: 0.122, 128: 0.378, 256: 0.437, 512: 0.063}\n")

    parser = argparse.ArgumentParser(description="Test different agents with command-line options.")
    parser.add_argument(
        "--agent", 
        choices=["expectimax", "mcts", "baseline"], 
        required=True,
        help="Type of agent to use (expectimax, mcts, or baseline)."
    )
    parser.add_argument(
        "--num_games", 
        type=int, 
        default=10, 
        help="Number of games to run (default: 10)."
    )
    parser.add_argument(
        "--depth", 
        type=int, 
        default=5, 
        help="Search depth for the agent (only used for expectimax, default: 5)."
    )
    
    # Parse arguments
    args = parser.parse_args()

    # Expectimax
    if args.agent == "expectimax":
        print(f"Running Expectimax agent for {args.num_games} games and depth {args.depth}.")
        expectimax.test_expectimax(args.num_games, args.depth)
    elif args.agent == "mcts":
        print(f"Running MCTS agent for {args.num_games} games.")
        mcts.test_mcts(args.num_games)
    elif args.agent == "baseline":
        print(f"Running baseline agent for {args.num_games} games.")
        baseline_agent.test_baseline_agent(args.num_games)
   








