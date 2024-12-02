import numpy as np
import random_play as rp
import cyclic_play as cp
import minimax as mm
import expectimax


if __name__ == "__main__":
    max_tile_results, score_results = rp.run_simulations(rp.simulate_game)
    print("Average Max Tile:", sum(max_tile_results) / len(max_tile_results))
    print("Tile Distribution:", {tile: max_tile_results.count(tile) for tile in set(max_tile_results)})

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

    num_games = 10
    depth = 3
    results = [expectimax.simulate_game_expectimax(depth) for _ in range(num_games)]
    max_tiles, scores = zip(*results)
    print(f"Average Max Tile: {np.mean(max_tiles)}")
    print(f"Average Score: {np.mean(scores)}")
   








