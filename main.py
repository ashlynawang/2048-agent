import numpy as np
import random_play as rp
import cyclic_play as cp
import minimax as mm
import expectimax
import time


if __name__ == "__main__":
    # max_tile_results, score_results = rp.run_simulations(rp.simulate_game)
    # print("Average Max Tile:", sum(max_tile_results) / len(max_tile_results))
    # print("Tile Distribution:", {tile: max_tile_results.count(tile) for tile in set(max_tile_results)})

    # # max tile from playing out each permutation of moves LRUD
    # cycle_max_results, cycle_score_results = cp.evaluate_all_cycles()
    # above_200_max = []
    # for cycle, score in cycle_max_results:
    #     print(f"Cycle: {cycle}, Max Tile: {max(score)}, Average Max Tile: {sum(score)/len(score)}")

    #Minimax
    # num_games = 30
    # depth = 3  # Adjust depth for performance
    # max_tile_results, score_results = mm.run_minimax_simulations(num_games, depth)
    # print(f"Average Max Tile: {np.mean(max_tile_results)}")
    # print(f"Tile Distribution: {np.unique(max_tile_results, return_counts=True)}")
    # print(f"Average Score: {np.mean(score_results)}")

    #Expectimax
    # grid = rp.init_grid()

    # while not rp.game_over(grid):
    #     best_move = expectimax.find_best_move(grid)
    #     if best_move:
    #         grid = best_move(grid)
    #         rp.add_new_tile(grid)
    #     else:
    #         break

    # print("Game Over!")
    # print("Max Tile:", np.max(grid))
    # print("Score:", np.sum(grid))

    # num_games = 20
    # depth = 4
    # results = [expectimax.simulate_game_expectimax(depth) for _ in range(num_games)]
    # max_tiles, scores = zip(*results)
    # print(f"Average Max Tile: {np.mean(max_tiles)}")
    # print(f"Average Score: {np.mean(scores)}")
    # print("Tile Distribution:", {tile: max_tiles.count(tile) for tile in set(max_tiles)})
    
    # num_simulations = 1  # Run 10 simulations
    # depth = 5  # Search depth for expectimax
    # start = time.time()
    # avg_max_tile, avg_score = expectimax.simulate_multiple_games(num_simulations, depth)
    # end = time.time()

    # print(f"Average Maximum Tile: {avg_max_tile}")
    # print(f"Average Score: {avg_score}")
    # print(end-start)

    num_games = 100  # Number of games to simulate
    depth = 4  # Search depth for Expectimax

    # Run simulations in parallel
    start = time.time()
    max_tiles, scores = expectimax.run_simulations_parallel(num_games, depth)
    end = time.time()

    # Calculate statistics
    avg_max_tile = np.mean(max_tiles)
    avg_score = np.mean(scores)

    print(f"Simulated {num_games} games.")
    print(f"Depth: {depth}")
    print(f"Average Maximum Tile: {avg_max_tile}")
    print(f"Tile Distribution: {np.unique(max_tiles, return_counts=True)}")
    print(end-start)

   








